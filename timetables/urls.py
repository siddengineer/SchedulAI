from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/create/', views.create_timetable, name='create_timetable'),
    path('timetables/<int:pk>/setup/', views.timetable_setup, name='timetable_setup'),
    path('timetables/<int:pk>/view/', views.timetable_view, name='timetable_view'),
    path('timetables/<int:pk>/delete/', views.delete_timetable, name='delete_timetable'),
    path('bells/', views.bell_list, name='bell_list'),
    path('bells/create/', views.create_bell, name='create_bell'),
    path('bells/<int:pk>/delete/', views.delete_bell, name='delete_bell'),
]
