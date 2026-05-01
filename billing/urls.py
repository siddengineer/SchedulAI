# from django.urls import path
# app_name = 'billing'
# urlpatterns = []
from django.urls import path
from django.http import HttpResponse

app_name = 'billing'

def upgrade(request):
    return HttpResponse("Upgrade page coming soon.")

urlpatterns = [
    path('upgrade/', upgrade, name='upgrade'),
]