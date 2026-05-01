from django.urls import path
from . import views
app_name = 'chatbot'
name = 'index'

urlpatterns = [
    path('', views.chatbot_home, name='chatbot'),
    path('send/', views.send_message, name='chatbot_send'),
    path('clear/<int:session_id>/', views.clear_session, name='chatbot_clear'),
]
