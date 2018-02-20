__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json
from itertools import groupby

from PIL import Image
from pprint import PrettyPrinter
from palettable.cmocean import sequential

#import plotly.offline as py
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from caretaking.models import Diary
from caretaking.models import TaskType

class Command(BaseCommand):
    help = "Make a graph"
    help += "Usage: django manage.py mkgraph > caretaking/sql/college.sql"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        
        """

        qs = Diary.objects.filter(staff__user__username='cousinsd').filter(day__year='2018')

        # group for tasktypes to stack in proportion to number of tasks per type
        # all adding up to the hours for the day
        traces = {}
        labels = {}
        for d in [{val: list()} for val in TaskType.objects.values_list('name', flat=True)]:
            traces.update(d)
            #labels.update(d)

        x = []

        for ob in qs:
            # compile x axis array
            x.append(ob.day)

            # get the tasktypes of tasks on this day
            tasktypes = list(ob.tasks.values_list('tasktype__name', flat=True))
            tasktypes.sort()

            # group the tasktypes and calculate as a fraction of the total hours for day
            # e.g. {'Duties': 4.0, 'Fields': 2.0, 'Gardens': 1.0} = 7 hours
            groups = {}
            for d in [{key: len(list(group))/len(tasktypes) * ob.hours} for key, group in
                    groupby(tasktypes)]:
                groups.update(d)

            # update the dict of traces with each day
            for name, array in traces.items():
                if name in groups.keys():
                    array.append(groups[name])
                    #labels[key].append(groups[key]/ob.hours * 100)
                else:
                    array.append(0.0)
                    #labels[key].append(0.0)

        pp = PrettyPrinter()
        data = []
        colors = sequential.Thermal_10.hex_colors
        step = 0
        for name, array in traces.items():
            data.append(go.Bar(
                x=x,
                y=array,
                name=name,
                marker=dict(color=colors[step]),
                ))
            step = step + 1

        title = 'Year to Date'
        layout = go.Layout(
            title=title,
            font=go.Font(
                family='Raleway, sans-serif'
                ),
            barmode='stack',
            showlegend=True,
            xaxis=go.XAxis(
                title='Day',
                tickangle=-45
                ),
            yaxis=go.YAxis(
                title='Hours'
                ),
            )
        layout.update(dict(
            shapes = [{
                'type': 'line',
                'x0': x[0],
                'x1': x[len(x) - 1],
                'y0': 8,
                'y1': 8,
                'opacity': 0.7,
                'line': {
                    'color': 'red',
                    'width': 1
                    }
                }]
            ))

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename=title)

        return

        # read from list comprehension to mark 'normal' working hours
        work_hours = pd.read_json(
                json.dumps(
                    [{
                        'day': ob.day,
                        'hours': 0 if ob.day.weekday() in [5, 6] or 
                        (ob.day.day < 15 and ob.day.month == 1) else 8
                    } for ob in qs ],
                    default=str
                    )
                )

        #img_path = 'my_first_figure.png'
        #py.image.save_as(fig, img_path)

        #img = Image.open(img_path)
        #img.show()
        return

