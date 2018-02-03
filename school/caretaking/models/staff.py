__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Staff(models.Model):
    """
    The member/s of staff assigned to the task in the case of an uncompleted task and the member/s
    of staff whom completed the task.

    Must be a django user of the application.::

        >>> from django.contrib.auth.models import User
        >>> darryl, created = User.objects.get_or_create(username='cousinsd', first_name='Darryl',
        ...     last_name='Cousins')
        >>> if created:
        ...     darryl.save()
        >>> caretaker, created = Staff.objects.get_or_create(user=darryl, title='Caretaker')
        >>> if created:
        ...     caretaker.save()
        >>> print(caretaker)
        Darryl Cousins (Caretaker)

    """
    staffid = models.AutoField(primary_key=True)
    title = models.CharField(
            max_length=50,
            help_text=_("The job title of this staff member"))
    comment = models.TextField(blank=True, null=True,
            help_text=_("Relevant useful information about this staff member"))
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE,
            help_text=_("The authentication backend user of the application"))

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        """Returns the person's full name and job title."""
        return '%s %s (%s)' % (
                self.user.first_name, self.user.last_name, self.title)

    def get_absolute_url(self):
        return reverse('staff-detail', kwargs={'username': self.user.username})
