__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

from PIL import Image

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from caretaking.models import Diary

class Command(BaseCommand):
    help = "Make a graph"
    help += "Usage: django manage.py mkgraph > caretaking/sql/college.sql"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        
        Uses a list of polygons to generate sql to insert CollegePlan MULTIPOLYGON object.
        """

        qs = Diary.objects.filter(day__year='2018')

        # read from list comprehension to mark 'normal' working hours
        work_hours = pd.read_json(
                json.dumps(
                    [{
                        'day': ob.day,
                        'hours': 0 if ob.day.weekday() in [5, 6] or ob.day.day < 7 else 8
                    } for ob in qs ],
                    default=str
                    )
                )

        for ob in qs:
            tasktypes = ob.tasks
            print(ob.day, tasktypes.values_list('tasktype__name', flat=True))
        return

        # read from database to mark actual worked hours
        hours_per_day = pd.read_json(
                json.dumps(
                    list(qs.values('day', 'hours')),
                    default=str
                    )
                )

        data = go.Data([
            go.Bar(
                x=hours_per_day['day'],
                y=hours_per_day['hours'],
                name='Hours worked',
                marker=go.Marker(
                    color='rgba(50, 171, 96, 0.7)',
                    line=go.Line(
                        color='rgba(50, 171, 96, 1.0)',
                        width=1,
                        )
                    )
                ),
            go.Bar(
                x=work_hours['day'],
                y=work_hours['hours'],
                name='Hours Due',
                marker=dict(
                    color='rgba(158, 202, 225, 0.2)',
                    line=dict(
                        color='rgba(8, 48, 107, 0.7)',
                        width=0.5,
                        )
                    )
                )
            ])
        layout = go.Layout(
            title=config['title'],
            font=go.Font(
                family='Raleway, sans-serif'
                ),
            barmode='overlay',
            showlegend=True,
            xaxis=go.XAxis(
                title='Day',
                tickangle=-45
                ),
            yaxis=go.YAxis(
                title='Hours'
                ),
            )
        fig = go.Figure(data=data, layout=layout)
        title = 'Year to Date'
        py.plot(fig, filename=title)

        img_path = 'my_first_figure.png'
        #py.image.save_as(fig, img_path)

        #img = Image.open(img_path)
        #img.show()
        return

