__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField

from caretaking.models import Staff

# Staff: first_name, last_name, title, username(hidden)
class StaffEditForm(forms.Form):
    """
        >>> data = {
        ...     'username': 'bleh',
        ...     'first_name': 'Jon',
        ...     'last_name': 'Doh',
        ...     'title': 'Rocker',
        ...    }
        >>> scf = StaffEditForm(data)
        >>> scf.is_valid()
        False
        >>> scf.errors
        {'username': ['User does not exist']}

        >>> data['username'] = 'cousinsd'
        >>> scf = StaffEditForm(data)
        >>> scf.is_valid()
        True
        >>> scf.save()

    """

    username = UsernameField(
        max_length=254,
        widget=forms.HiddenInput(),
    )
    first_name = forms.CharField(
        label='First name',
        required=True,
        max_length=50
    )
    last_name = forms.CharField(
        label='Last name',
        required=True,
        max_length=50
    )
    title = forms.CharField(
        label='Title',
        required=True,
        max_length=50
    )
    comment = forms.CharField(
        label='Comment',
        required=False,
        max_length=1024,
        widget=forms.TextInput(),
    )

    def save(self):
        """
        Save this form's Staff object.
        """
        if not self.user:
            raise ValueError(
                "No user found for Staff form"
            )
        if self.errors:
            raise ValueError(
                "The Staff object could not be edited because the data didn't validate."
            )

        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']

        try:
            staff = Staff.objects.get(user=self.user)
            staff.title = self.cleaned_data['title']
            staff.comment = self.cleaned_data['comment']
        except Staff.DoesNotExist:
            staff = Staff(
                user=self.user_instance,
                title=self.cleaned_data['title'],
                comment=self.cleaned_data['comment'],
            )

        staff.save()
        self.user.save()
        return staff

    save.alters_data = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            self.user= User.objects.get(username=username)
        except:
            raise forms.ValidationError(
                'User does not exist',
                code='user_does_not_exist',
            )
        return username
