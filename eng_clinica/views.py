from django.shortcuts import render

# Create your views here.


def engenharia_clinica(request):
    return render(request, 'engenharia/dashboard.html')
