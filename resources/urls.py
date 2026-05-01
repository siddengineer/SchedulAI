from django.urls import path
from . import views
app_name = 'resources'
name = 'list'
urlpatterns = [
    path('', views.resources_home, name='resources'),
    path('add-grade/', views.add_grade, name='add_grade'),
    path('add-room/', views.add_room, name='add_room'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('delete-grade/<int:pk>/', views.delete_grade, name='delete_grade'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete_room'),
    path('delete-subject/<int:pk>/', views.delete_subject, name='delete_subject'),
    # path('grade/add/', views.add_grade, name='add_grade'),
]
