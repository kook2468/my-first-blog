# Chart/urls.py
from django.contrib import admin
from django.urls import path
from chart import views                                     # !!!

urlpatterns = [
    path('', views.home, name='home'),
    path('covid_19/',
         views.covid_19, name='covid_19'),
    path('covid_confirmed/',
         views.covid_confirmed, name="covid_confirmed"),
    path('covid_recovered/',
         views.covid_recovered, name="covid_recovered"),
    path('covid_deaths/',
         views.covid_deaths, name="covid_deaths"),
    path('ticket-class/1/',
         views.ticket_class_view_1, name='ticket_class_view_1'),
    path('ticket-class/2/',
         views.ticket_class_view_2, name='ticket_class_view_2'),
    path('ticket-class/3/',
         views.ticket_class_view_3, name='ticket_class_view_3'),
    path('world-population/',
         views.world_population, name='world_population'),  # !!!
    path('json-example/', views.json_example, name='json_example'),
    path('json-example/data/', views.chart_data, name='chart_data'),
]