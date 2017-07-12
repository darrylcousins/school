__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.list import BaseListView, MultipleObjectMixin
from django.views.generic import DetailView

from metrel.models import Appliances

from django.http import JsonResponse


class BSGridField(object):
    """Create a field-like object from columns sent from ``bs_grid`` json post request.

    These fields are then used to refine the django view queryset.
    """

    def __init__(self, data={}):
        print(data)


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
    def get(self, request, *args, **kwargs):
        return self.render_to_response(request)

    def post(self, request, *args, **kwargs):
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
        rows_per_page = data.get('rows_per_page', self.paginate_by)
        page_num = data.get('page_num', 1)
        debug_mode = data.get('debug_mode', 'no')
        # translating bs_grid ``columns`` to django ``fields``
        fields = [BSGridField(column) for column in data.get('columns', [])]
        sorting = data.get('sorting', [])
        filter_rules = data.get('filter_rules', [])

        # set self.kwargs value used by in ``MultipleObjectMixin.paginate_queryset``
        self.kwargs[self.page_kwarg] = page_num

        # get a paginated queryset from django generic view MultipleObjectMixin
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.queryset, rows_per_page)
        context['page_data'] = [s['fields'] for s in serializers.serialize('python', queryset)]
        return context


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
        ...             "order": "ascending"
        ...         }
        ...     ],
        ...     "filter_rules": [],
        ...     "debug_mode": "no"              
        ... }'''
        >>> response = client.post(reverse('json-appliance-list'), data, content_type="application/json")
        >>> print(response)


    """
    queryset = Appliances.objects.order_by('appliancetag')
    context_object_name = 'appliances'
    paginate_by = 10

