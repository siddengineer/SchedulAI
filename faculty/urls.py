from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_list, name='faculty_list'),
    path('add/', views.add_faculty, name='add_faculty'),
    path('edit/<int:pk>/', views.edit_faculty, name='edit_faculty'),
    path('delete/<int:pk>/', views.delete_faculty, name='delete_faculty'),
    path('leave/<int:pk>/', views.add_leave, name='add_leave'),
]
