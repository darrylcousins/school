__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json
from distutils.util import strtobool

from django.core import serializers
from django.utils import six
from django.views.generic import ListView
from django.views.generic.list import BaseListView, MultipleObjectMixin
from django.views.generic import DetailView

from metrel.models import Appliances

from django.http import JsonResponse


class BSCondition(object):
    """Create an object to contain condition values as prescribed by bs_grid and passed in ajax
    request"""
    filter_type = ''
    number_type = None # used for filter_type = 'number'
    fiter_value = []
    operator = ''

    def __init__(self, filter_type, operator, filter_value, number_type=None):
        self.filter_type = filter_type
        self.operator = operator
        self.filter_value = filter_value
        self.number_type = number_type


class BSGridField(object):
    """Create a field-like object from columns sent from ``bs_grid`` json post request.

    These fields are then used to refine the django view queryset.
    """
    field = ''
    header = ''
    sortable = False
    order = None
    visible = True
    conditions = []

    def __init__(self, data={}):
        """
        Convert given dictionary to object attributes, pretty much accept everything passed
        """
        for key, item in data.items():

            # convert 'yes', 'no' to python bool
            if item in ('yes', 'no'):
                item = bool(strtobool(item))

            # set self.'attribute'
            setattr(self, key, item)
            data[key] = item
        # print(data)

    def __str__(self):
        return self.field


class BSGridJSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response consumable by bs_grid jquery plugin.
 
    $result = array(
			'total_rows' => null,
			'page_data' => null,
			'error' => null,
			'filter_error' => array(),
			'debug_message' => array()
		);

    """
    # value set from bs_grid values and created in `get_data`
    fields = {}

    def get(self, request, *args, **kwargs):
        return self.render_to_response(request)

    def post(self, request, *args, **kwargs):
        # reset self.fields
        self.fields = {}
        return self.get(request, *args, **kwargs)

    def render_to_response(self, request, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        # import pdb; pdb.set_trace()
        return JsonResponse(
            self.get_data(request),
            **response_kwargs
        )

    def get_data(self, request, context={}):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        context = {
                'total_rows': 0,
                'page_data': [],
                'error': None,
                'filter_error': [],
                'debug_message': []
                }
        context['total_rows'] = len(self.queryset)

        data = json.loads(request.body)

        # collect bs_grid ajax post values

        debug_mode = data.get('debug_mode', 'no')

        # translating bs_grid ``columns`` to django ``fields``
        self.fields = dict([(column['field'], BSGridField(column)) for column in data.get('columns', [])])

        # pull in bs_grid sorting rules into field objects
        # used by `self.get_ordering` to define ordering
        for order in data.get('sorting', []):
            if order['field'] in self.fields.keys():
                self.fields[order['field']].order = order['order']

        # pull in bs_grid filter rules into field objects
        filter_rules = data.get('filter_rules', [])

        for rule in data.get('filter_rules'):
            condition = rule['condition']
            if condition['field'] in self.fields.keys():
                print(self.fields[condition['field']])
                self.fields[condition['field']].conditions.append(
                    BSCondition(
                        condition['filterType'],
                        condition['operator'],
                        condition['filterValue']
                        )
                    )

        # set self.kwargs value used by in ``MultipleObjectMixin.paginate_queryset``
        self.kwargs[self.page_kwarg] = data.get('page_num', 1)

        # get a paginated queryset from django generic view MultipleObjectMixin
        paginator, page, queryset, is_paginated = self.paginate_queryset(
                self.get_queryset(), data.get('rows_per_page', self.paginate_by))
        context['page_data'] = [s['fields'] for s in serializers.serialize('python', queryset)]
        return context

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        queryset = super(BSGridJSONResponseMixin, self).get_queryset()
        for (key, field) in self.fields.items():
            condition = None
            if len(field.conditions):
                print(key, field.conditions)
                for condition in field.conditions:
                    print(key, condition.filter_type, condition.filter_value)
        return queryset

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        
        Over ride parent method to used self.fields
        """
        # django set a default with this algorithm
#        ordering = self.ordering
#        if isinstance(ordering, six.string_types):
#            ordering = [ordering,]
#        else:
#            ordering = list(ordering)

        # ignoring django default
        ordering = []

        # use self.fields created in self.get_data
        for (key, field) in self.fields.items():
            if field.sortable:
                if field.order == 'ascending':
                    if key not in ordering:
                        ordering.append(key)
                elif field.order == 'descending':
                    if "-" + key not in ordering:
                        ordering.append("-" + key)
        return tuple(ordering)


class ApplianceList(ListView):
    queryset = Appliances.objects.order_by('appliancetag')
    template_name = 'appliance_list.html'
    context_object_name = 'appliances'
    paginate_by = 10


class JSONApplianceList(BSGridJSONResponseMixin, BaseListView):
    """
    Set up test client::

        >>> from django.test import Client
        >>> from django.core.urlresolvers import reverse
        >>> client = Client()

    Find our diary day for this set of tasks::

        >>> from django.core.management import call_command
        >>> call_command("loaddata", 'initial', database='metrel', app='metrel', verbosity=0)

        >>> import json
        >>> data = '''{
        ...     "page_num": "1",
        ...     "rows_per_page": "10",
        ...     "columns": [
        ...         {
        ...             "field": "appliancetag",
        ...             "header": "Tag",
        ...             "visible": "yes",
        ...             "sortable": "yes"
        ...         },
        ...         {
        ...             "field": "location",
        ...             "header": "Location"
        ...         },
        ...         {
        ...             "field": "comment",
        ...             "header": "Appliance"
        ...         }
        ...     ],
        ...     "sorting": [
        ...         {
        ...             "sortingName": "Tag",
        ...             "field": "appliancetag",
        ...             "order": "descending"
        ...         }
        ...     ],
        ...     "debug_mode": "no"              
        ... }'''
        >>> response = client.post(reverse('json-appliance-list'), data, content_type="application/json")
        >>> print(response)
        <JsonResponse status_code=200, "application/json">
        >>> print(response.content)


    """
    queryset = Appliances.objects.all()
    context_object_name = 'appliances'
    paginate_by = 10

