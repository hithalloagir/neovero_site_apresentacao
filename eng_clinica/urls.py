from django.urls import path
from . import views

app_name = 'eng_clinica'

urlpatterns = [
    path('', views.engenharia_clinica, name='dashboard_eng_clinica'),
]
