from django.shortcuts import render
from datetime import datetime, timedelta
import calendar
from .forms import GraficoFilterForm
from .services.graficos.graficos_dashboards import get_tempo_medio_atendimento_por_unidade, get_dispersao_reparo_atendimento


def home(request):
    return render(request, 'engenharia/home.html')


def engenharia_clinica_graficos(request):
    # 1. Pega os dados da URL (GET)
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    empresa = request.GET.get('empresa')

    # 2. Configura o formulário com os dados atuais (para não sumir depois de filtrar)
    form = GraficoFilterForm(initial={
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'empresa': empresa
    })

    # 3. Variáveis de Resultado começam VAZIAS (Padrão Rígido)
    labels_atendimento = []
    data_atendimento = []
    dados_scatter = []

    # 4. O GUARDIÃO (A Regra Rígida)
    # Só executa a busca se TIVER data_inicio E data_fim preenchidos
    if data_inicio and data_fim:

        # Chama o serviço do Gráfico de Barras
        labels_atendimento, data_atendimento = get_tempo_medio_atendimento_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Dispersão
        dados_scatter = get_dispersao_reparo_atendimento(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

    # 5. Passa para o template (Se não entrou no if, vai tudo vazio)
    context = {
        'form': form,
        'labels_atendimento': labels_atendimento,
        'data_atendimento': data_atendimento,
        'dados_scatter': dados_scatter,

        # Seus outros gráficos (Tasks/Email) também devem seguir essa lógica se existirem
        'tasks_labels': [],
        'tasks_data': [],
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
