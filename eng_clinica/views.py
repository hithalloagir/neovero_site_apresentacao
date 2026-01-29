from django.shortcuts import render
from datetime import datetime, timedelta
import calendar
from .forms import GraficoFilterForm
from .services.graficos.graficos_dashboards import (
    get_tempo_medio_atendimento_por_unidade,
    get_dispersao_reparo_atendimento,
    get_tempo_medio_reparo_por_unidade,
    get_taxa_cumprimento_por_unidade,
    get_qtde_os_por_tipo_manutencao,
    get_qtde_os_planejadas_realizadas,
    get_qtde_os_planejadas_n_realizadas,
    get_os_taxa_conclusao_planejamento,
    get_taxa_disponibilidade_equipamentos,
    get_qtde_equipamentos_por_unidade,
    get_idade_media_equipamentos_por_unidade,
    get_idade_media_equipamentos_por_familia,
    get_maiores_tempos_reparo_criticos_por_familia,
    get_principais_causas_corretivas,
    get_maiores_tempos_parada_criticos_por_familia,
    get_tempo_mediano_parada_criticos_por_unidade,
    get_matriz_indisponibilidade_criticos,
    get_taxa_disponibilidade_equipamentos_criticos,
    get_qtde_equipamentos_criticos_por_unidade,
    get_tempo_primeiro_atendimento_critico,
)


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

    labels_reparo = []
    data_reparo = []

    labels_taxa_cumprimento_medio = []
    data_taxa_cumprimento_medio = []
    qtd_fechada = []
    total_os = []
    taxa_cumprimento_metadados = []

    labels_tipo_manutencao_os = []
    data_tipo_manutencao_os = []

    labels_qtde_os_planejadas_realizadas = []
    data_qtde_os_planejadas_realizadas = []

    labels_qtde_os_planejadas_n_realizadas = []
    data_qtde_os_planejadas_n_realizadas = []

    labels_os_taxa_conclusao_planejamento = []
    data_os_taxa_conclusao_planejamento = []
    qtde_os_taxa_conclusao_planejamento = []
    total_os_taxa_conclusao_planejamento = []
    plan_taxa_metadados = []

    labels_disponibilidade_equipamentos = []
    data_disponibilidade_equipamentos = []

    labels_equipamentos_unidade = []
    data_equipamentos_unidade = []

    labels_idade_equipamentos_unidade = []
    data_idade_equipamentos_unidade = []

    labels_idade_media_equipamentos_familia = []
    data_idade_media_equipamentos_familia = []

    labels_reparo_tempo_critico = []
    data_reparo_tempo_critico = []

    labels_principais_causas_corretivas = []
    data_principais_causas_corretivas = []

    labels_maiores_tempos_parada_criticos_por_familia = []
    data_maiores_tempos_parada_criticos_por_familia = []

    labels_tempo_mediano_parada_criticos_por_unidade = []
    data_tempo_mediano_parada_criticos_por_unidade = []

    pivot_indisponibilidade_equipamentos_criticos = {}

    labels_taxa_disponibilidade_equipamentos_criticos = []
    data_taxa_disponibilidade_equipamentos_criticos = []

    labels_equipamentos_criticos_por_unidade = []
    data_equipamentos_criticos_por_unidade = []

    labels_primeiro_atendimento_equipamento_critico = []
    data_primeiro_atendimento_equipamento_critico = []

    # 4. Lógica de Filtragem
    # Só executa a busca se tiver data_inicio e data_fim preenchidos
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

        # Chama o serviço do Gráfico de Barras para Tempo Médio de Reparo por Unidade (dia)
        labels_reparo, data_reparo = get_tempo_medio_reparo_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Taxa de Cumprimento por Unidade (percentual)
        labels_taxa_cumprimento_medio, data_taxa_cumprimento_medio, qtd_fechada, total_os = get_taxa_cumprimento_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        if labels_taxa_cumprimento_medio:
            for fechada, total in zip(qtd_fechada, total_os):
                taxa_cumprimento_metadados.append({
                    'fechada': fechada,
                    'total': total,
                })

        # Chama o serviço do Gráfico de Quantidade de OS por Tipo de Manutenção
        labels_tipo_manutencao_os, data_tipo_manutencao_os = get_qtde_os_por_tipo_manutencao(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Quantidade de OS Planejadas Realizadas
        labels_qtde_os_planejadas_realizadas, data_qtde_os_planejadas_realizadas = get_qtde_os_planejadas_realizadas(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Quantidade de OS Planejadas Não Realizadas
        labels_qtde_os_planejadas_n_realizadas, data_qtde_os_planejadas_n_realizadas = get_qtde_os_planejadas_n_realizadas(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Taxa de Conclusão de Planejamento
        labels_os_taxa_conclusao_planejamento, data_os_taxa_conclusao_planejamento, qtde_os_taxa_conclusao_planejamento, total_os_taxa_conclusao_planejamento = get_os_taxa_conclusao_planejamento(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        if labels_os_taxa_conclusao_planejamento:
            for qtde_fechada, total in zip(qtde_os_taxa_conclusao_planejamento, total_os_taxa_conclusao_planejamento):
                plan_taxa_metadados.append({
                    'fechada': qtde_fechada,
                    'total': total,
                })

        # Chama o serviço do Gráfico de Taxa de Disponibilidade de Equipamentos
        labels_disponibilidade_equipamentos, data_disponibilidade_equipamentos = get_taxa_disponibilidade_equipamentos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Quantidade de Equipamentos por Unidade
        labels_equipamentos_unidade, data_equipamentos_unidade = get_qtde_equipamentos_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Idade Média dos Equipamentos por Unidade
        labels_idade_equipamentos_unidade, data_idade_equipamentos_unidade = get_idade_media_equipamentos_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Idade Média dos Equipamentos por Família
        labels_idade_media_equipamentos_familia, data_idade_media_equipamentos_familia = get_idade_media_equipamentos_por_familia(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Maiores tempos de reparo de equipamentos criticos por familia (h)
        labels_reparo_tempo_critico, data_reparo_tempo_critico = get_maiores_tempos_reparo_criticos_por_familia(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico de Principais causas corretivas
        labels_principais_causas_corretivas, data_principais_causas_corretivas = get_principais_causas_corretivas(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o serviço do Gráfico dos Maiores tempos de parada de Equipamentos criticos por familia
        labels_maiores_tempos_parada_criticos_por_familia, data_maiores_tempos_parada_criticos_por_familia = get_maiores_tempos_parada_criticos_por_familia(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o Serviço do Gráfico do Tempo mediano de parada de equipamentos criticos das unidades
        labels_tempo_mediano_parada_criticos_por_unidade, data_tempo_mediano_parada_criticos_por_unidade = get_tempo_mediano_parada_criticos_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o Serviço do Gráfico de Horarios que os equipamentos criticos ficaram indisponiveis
        pivot_indisponibilidade_equipamentos_criticos = get_matriz_indisponibilidade_criticos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o Serviço do Gráfico Taxa de Disponibilidade Dos Equipamentos Críticos
        labels_taxa_disponibilidade_equipamentos_criticos, data_taxa_disponibilidade_equipamentos_criticos = get_taxa_disponibilidade_equipamentos_criticos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o Serviço do Gráfico Quantidade de Equipamentos Criticos por Unidade
        labels_equipamentos_criticos_por_unidade, data_equipamentos_criticos_por_unidade = get_qtde_equipamentos_criticos_por_unidade(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

        # Chama o Serviço do Gráfico Tempo do Primeito Atendimento de Equipamento Critico
        labels_primeiro_atendimento_equipamento_critico, data_primeiro_atendimento_equipamento_critico = get_tempo_primeiro_atendimento_critico(
            data_inicio=data_inicio,
            data_fim=data_fim,
            empresa=empresa
        )

    # 5. Passa para o template (Se não entrou no if, vai tudo vazio)
    context = {
        'form': form,
        # Gráfico de Tempo Médio de Atendimento por Unidade
        'labels_atendimento': labels_atendimento,
        'data_atendimento': data_atendimento,

        # Gráfico de Dispersão (Scatter Plot)
        'dados_scatter': dados_scatter,

        # Gráfico de Tempo Médio de Reparo por Unidade (dia)
        'labels_reparo': labels_reparo,
        'data_reparo': data_reparo,

        # Gráfico de Taxa de Cumprimento por Unidade (percentual)
        'labels_taxa_cumprimento_medio': labels_taxa_cumprimento_medio,
        'data_taxa_cumprimento_medio': data_taxa_cumprimento_medio,
        'taxa_cumprimento_metadados': taxa_cumprimento_metadados,

        # Gráfico de Quantidade de OS por Tipo de Manutenção
        'labels_tipo_manutencao_os': labels_tipo_manutencao_os,
        'data_tipo_manutencao_os': data_tipo_manutencao_os,

        # Gráfico de Quantidade de OS Planejadas Realizadas
        'labels_qtde_os_planejadas_realizadas': labels_qtde_os_planejadas_realizadas,
        'data_qtde_os_planejadas_realizadas': data_qtde_os_planejadas_realizadas,

        # Gráfico de Quantidade de OS Planejadas Não Realizadas
        'labels_qtde_os_planejadas_n_realizadas': labels_qtde_os_planejadas_n_realizadas,
        'data_qtde_os_planejadas_n_realizadas': data_qtde_os_planejadas_n_realizadas,

        # Gráfico de OS Taxa de Conclusão de Planejamento
        'labels_os_taxa_conclusao_planejamento': labels_os_taxa_conclusao_planejamento,
        'data_os_taxa_conclusao_planejamento': data_os_taxa_conclusao_planejamento,
        'plan_taxa_metadados': plan_taxa_metadados,

        # Gráfico de Taxa de Disponibilidade de Equipamentos
        'labels_disponibilidade_equipamentos': labels_disponibilidade_equipamentos,
        'data_disponibilidade_equipamentos': data_disponibilidade_equipamentos,

        # Gráfico de Quantidade de Equipamentos por Unidade
        'labels_equipamentos_unidade': labels_equipamentos_unidade,
        'data_equipamentos_unidade': data_equipamentos_unidade,

        # Gráfico de Idade Média dos Equipamentos por Unidade
        'labels_idade_equipamentos_unidade': labels_idade_equipamentos_unidade,
        'data_idade_equipamentos_unidade': data_idade_equipamentos_unidade,

        # Gráfico de Idade Média dos Equipamentos por Família
        'labels_idade_media_equipamentos_familia': labels_idade_media_equipamentos_familia,
        'data_idade_media_equipamentos_familia': data_idade_media_equipamentos_familia,

        # Gráfico de Maiores tempos de reparo de equipamentos criticos por familia (h)
        'labels_reparo_tempo_critico': labels_reparo_tempo_critico,
        'data_reparo_tempo_critico': data_reparo_tempo_critico,

        # Gráfico de Principais causas Corretivas
        'labels_principais_causas_corretivas': labels_principais_causas_corretivas,
        'data_principais_causas_corretivas': data_principais_causas_corretivas,

        # Gráfico de Maiores Tempos de parada equipamentos criticos por familia
        'labels_maiores_tempos_parada_criticos_por_familia': labels_maiores_tempos_parada_criticos_por_familia,
        'data_maiores_tempos_parada_criticos_por_familia': data_maiores_tempos_parada_criticos_por_familia,

        # Gráfico de Tempo Mediano de paradas de equipamentos criticos por unidade
        'labels_tempo_mediano_parada_criticos_por_unidade': labels_tempo_mediano_parada_criticos_por_unidade,
        'data_tempo_mediano_parada_criticos_por_unidade': data_tempo_mediano_parada_criticos_por_unidade,

        # Gráfico de Horarios que os equipamentos criticos ficaram indisponiveis
        'pivot_indisponibilidade_equipamentos_criticos': pivot_indisponibilidade_equipamentos_criticos,

        # Gráfico Taxa de Disponibilidade Dos Equipamentos Críticos
        'labels_taxa_disponibilidade_equipamentos_criticos': labels_taxa_disponibilidade_equipamentos_criticos,
        'data_taxa_disponibilidade_equipamentos_criticos': data_taxa_disponibilidade_equipamentos_criticos,

        # Gráfico Quantidade de Equipamentos Criticos Por Unidade
        'labels_equipamentos_criticos_por_unidade': labels_equipamentos_criticos_por_unidade,
        'data_equipamentos_criticos_por_unidade': data_equipamentos_criticos_por_unidade,

        # Gráfico Tempo do Primeito Atendimento de Equipamento Critico
        'labels_primeiro_atendimento_equipamento_critico': labels_primeiro_atendimento_equipamento_critico,
        'data_primeiro_atendimento_equipamento_critico': data_primeiro_atendimento_equipamento_critico,
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
