from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'engenharia/home.html')


def engenharia_clinica_graficos(request):
    context = {
        "daily_sales_labels": ["M", "T", "W", "T", "F", "S", "S"],
        "daily_sales_data": [8, 12, 3, 11, 18, 13, 32],

        "email_labels": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
        "email_data": [420, 350, 220, 650, 450, 360, 240, 340, 460, 510, 630, 780],

        "tasks_labels": ["12p", "3p", "6p", "9p", "12a", "3a", "6a", "9a"],
        "tasks_data": [120, 640, 360, 200, 180, 150, 110, 90],
    }
    return render(request, 'engenharia/graficos.html', context)


def engenharia_clinica_indicadores(request):
    context = {
        "daily_sales_labels": ["M", "T", "W", "T", "F", "S", "S"],
        "daily_sales_data": [8, 12, 3, 11, 18, 13, 32],

        "email_labels": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
        "email_data": [420, 350, 220, 650, 450, 360, 240, 340, 460, 510, 630, 780],

        "tasks_labels": ["12p", "3p", "6p", "9p", "12a", "3a", "6a", "9a"],
        "tasks_data": [120, 640, 360, 200, 180, 150, 110, 90],
    }
    return render(request, 'engenharia/indicadores.html', context)
