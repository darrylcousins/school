__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.models import User

from caretaking.models import Diary
from caretaking.models import Staff

class DiaryList(ListView):
    queryset = Diary.objects.order_by('-day')
    template_name = 'diary_list.html'


class StaffDiaryList(ListView):
    template_name = 'staff_diary_list.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDiaryList, self).get_context_data(**kwargs)
        context['staff'] = self.staff
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.args[0])
        self.staff = get_object_or_404(Staff, user=self.user)
        return Diary.objects.filter(staff=self.staff).order_by('-day')


class DiaryDetailView(DetailView):
    queryset = Diary.objects.all()
    template_name = 'diary_detail.html'

    def get_object(self):
        object = super(DiaryDetailView, self).get_object()
        return object
