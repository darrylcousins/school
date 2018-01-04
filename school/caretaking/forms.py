__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django import forms


class DiaryForm(forms.Form):
    """Diary form to filter diary selection::

        >>> f = DiaryForm()

    Unused - using simple template and logic in TaskList and DiaryList views.

    TODO consider refractoring to use form and move logic here.
    """
    search = forms.CharField(label='Search', max_length=100)
