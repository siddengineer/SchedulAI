# ============================================================
# dashboard/urls.py
# ============================================================

# from django.urls import path
# from . import views

# app_name = 'dashboard'

# urlpatterns = [
#     path('',     views.DashboardView.as_view(), name='home'),
# ]

from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]