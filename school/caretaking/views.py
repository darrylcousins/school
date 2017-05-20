__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.gis import gdal, geos

from caretaking.models import Diary, Staff, Location

class DiaryList(ListView):
    queryset = Diary.objects.order_by('-day')
    template_name = 'diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10


class StaffDiaryList(ListView):
    template_name = 'staff_diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.args[0])
        self.staff = get_object_or_404(Staff, user=self.user)
        return Diary.objects.filter(staff=self.staff).order_by('-day')

    def get_context_data(self, **kwargs):
        context = super(StaffDiaryList, self).get_context_data(**kwargs)
        context['staff'] = self.staff
        return context


class DiaryDetail(DetailView):
    queryset = Diary.objects.all()
    template_name = 'diary_detail.html'
    context_object_name = 'diary'

    def get_object(self):
        obj = super(DiaryDetail, self).get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DiaryDetail, self).get_context_data(**kwargs)
        context['staff'] = self.object.staff
        try:
            value = Location.objects.get(name="CollegePlan").polygon
            context['college_wkt'] = geos.GEOSGeometry(value).wkt
        except Location.DoesNotExist:
            context['college_wkt'] = ''
        geometry = None
        for task in self.object.tasks:
            if geometry is None:
                # initialize geosgeometry object
                geometry = geos.GEOSGeometry(task.point)
            else:
                geometry = geometry.union(geos.GEOSGeometry(task.point))
        context['diary_wkt'] = geometry.wkt

        return context
