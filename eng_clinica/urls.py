from django.urls import path
from . import views

app_name = 'eng_clinica'

urlpatterns = [
    path('graficos/', views.engenharia_clinica_graficos, name='graficos_eng_clinica'),
    path('indicadores/', views.engenharia_clinica_indicadores, name='indicadores_eng_clinica'),
]
