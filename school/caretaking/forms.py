__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django import forms


class DiaryForm(forms.Form):
    """Diary form to filter diary selection::

        >>> f = DiaryForm()
        >>> print(f)

    """
    search = forms.CharField(label='Search', max_length=100)
