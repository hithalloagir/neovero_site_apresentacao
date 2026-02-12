import pandas as pd
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.utils import timezone

# Importando Models do outro App
from eng_clinica.models import ConsultaOsNew, ConsultaEquipamentos

from eng_clinica.services.dashboard_home.dashboard import (
    get_evolucao_backlog_metrologia,
    get_evolucao_backlog_manutencoes_corretivas,
    get_total_servicos_realizados,
    get_quantidade_equipamentos_cadastrados,
    get_disponibilidade_total,
    get_detalhes_equipamentos_parados,
    get_equipamentos_criticos_indisponiveis_os,
    get_detalhes_equipamentos_criticos_indisponiveis,
)


def home(request):
    start_total = time.time()
    hoje = timezone.now()

    # ---------------------------------------------------------
    # 1. FILTRO DE EMPRESA
    # ---------------------------------------------------------
    empresas_disponiveis = ConsultaOsNew.objects.exclude(empresa__isnull=True).exclude(empresa='').values_list('empresa', flat=True).distinct().order_by('empresa')
    empresa_selecionada = request.GET.get('empresa')

    # ---------------------------------------------------------
    # 2. CARREGAMENTO DE DADOS (OS)
    # ---------------------------------------------------------
    # Limita a busca aos últimos 24 meses para otimização
    data_limite_historico = hoje - relativedelta(months=48)

    qs_os_base = ConsultaOsNew.objects.filter(abertura__gte=data_limite_historico)

    if empresa_selecionada:
        qs_os_base = qs_os_base.filter(empresa=empresa_selecionada)

    # Definindo colunas essenciais para o DataFrame de OS
    cols_os = [
        'os', 'tag', 'empresa', 'abertura', 'fechamento',
        'situacao', 'tipomanutencao', 'prioridade', 'parada', 'causa',
        'local_api',
    ]
    df_os = pd.DataFrame(list(qs_os_base.values(*cols_os)))

    # ---------------------------------------------------------
    # 3. CARREGAMENTO DE DADOS (EQUIPAMENTOS) - NOVO BLOCO
    # ---------------------------------------------------------
    qs_equip_base = ConsultaEquipamentos.objects.all()

    if empresa_selecionada:
        qs_equip_base = qs_equip_base.filter(empresa=empresa_selecionada)

    cols_equip = ['tag', 'empresa', 'tipoequipamento', 'modelo']

    # Cria o DataFrame de Equipamentos
    df_equip = pd.DataFrame(list(qs_equip_base.values(*cols_equip)))

    # ---------------------------------------------------------
    # 4. PRÉ-PROCESSAMENTO
    # ---------------------------------------------------------
    if not df_os.empty:
        for col in ['abertura', 'fechamento', 'parada']:
            if col in df_os.columns:
                df_os[col] = pd.to_datetime(df_os[col], errors='coerce')

    # ---------------------------------------------------------
    # 5. GERAÇÃO DOS GRÁFICOS
    # ---------------------------------------------------------

    # Gráfico 1: Metrologia (Segue normal, só usa df_os)
    labels_backlog, data_backlog = get_evolucao_backlog_metrologia(df_os, df_equip)

    # Gráfico 2: Corretivas (AGORA RECEBE df_equip TAMBÉM)
    # A função vai usar o df_equip para filtrar o que é Equipamento Médico
    labels_backlog_corretivas, data_backlog_corretivas = get_evolucao_backlog_manutencoes_corretivas(df_os, df_equip)

    # Gráfico 3: Total Realizado (Segue normal)
    labels_backlog_total_servicos, data_backlog_total_servicos = get_total_servicos_realizados(df_os, df_equip)

    # KPI: Quantidade de Equipamentos Cadastrados
    total_equipamentos_medicos = get_quantidade_equipamentos_cadastrados(df_equip)

    # KPI: Disponibilidade Total
    kpi_disp_pct, kpi_disp_qtd, kpi_disp_total = get_disponibilidade_total(df_os, df_equip)

    # LISTA AG GRID (Detalhes)
    lista_equipamentos_parados = get_detalhes_equipamentos_parados(df_os, df_equip)

    # KPI Equipamentos Críticos Indisponíveis
    qtd_criticos_parados = get_equipamentos_criticos_indisponiveis_os(df_os, df_equip)

    # LISTA AG GRID (Detalhes)
    lista_equipamentos_criticos_indisponiveis = get_detalhes_equipamentos_criticos_indisponiveis(df_os, df_equip)

    # ---------------------------------------------------------
    # 6. CONTEXTO FINAL
    # ---------------------------------------------------------
    context = {
        # Filtro de empresas para o template
        'empresas_disponiveis': empresas_disponiveis,
        'empresa_selecionada': empresa_selecionada,

        # Gráficos
        'labels_backlog': labels_backlog,
        'data_backlog': data_backlog,

        'labels_backlog_corretivas': labels_backlog_corretivas,
        'data_backlog_corretivas': data_backlog_corretivas,

        'labels_backlog_total_servicos': labels_backlog_total_servicos,
        'data_backlog_total_servicos': data_backlog_total_servicos,

        # KPI Numérico
        'total_equipamentos_medicos': total_equipamentos_medicos,

        # KPI de Disponibilidade TOTAL
        'kpi_disp_pct': kpi_disp_pct,
        'kpi_disp_qtd': kpi_disp_qtd,
        'kpi_disp_total': kpi_disp_total,

        'lista_equipamentos_parados': lista_equipamentos_parados,

        # KPI Equipamentos Críticos Indisponíveis
        'qtd_criticos_parados': qtd_criticos_parados,
        'lista_equipamentos_criticos_indisponiveis': lista_equipamentos_criticos_indisponiveis,
    }

    print(f"🚀 [HOME] Tempo total de carga: {time.time() - start_total:.4f}s")
    return render(request, 'core/home.html', context)
