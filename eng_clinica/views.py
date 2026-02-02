import pandas as pd
from django.shortcuts import render
from datetime import datetime
from .forms import GraficoFilterForm
from .models import ConsultaOs, ConsultaEquipamentos

# Importa as funções refatoradas
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

from .services.indicadores.indicadores_dashboards import (
    get_total_equipamentos_cadastrados,
    get_total_os_corretivas,
    get_maiores_causas_corretivas,
    get_mtbf_medio_kpi,
    get_mttr_kpi,
    get_tempo_medio_primeiro_atendimento_kpi,
    get_tempo_mediano_primeiro_atendimento_kpi,
)


def home(request):
    return render(request, 'engenharia/home.html')


def engenharia_clinica_graficos(request):
    # ---------------------------------------------------------
    # 1. Configuração de Datas e Filtros Iniciais
    # ---------------------------------------------------------
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)

    str_hoje = hoje.strftime('%Y-%m-%d')
    str_inicio_mes = inicio_mes.strftime('%Y-%m-%d')

    # Pega da URL ou usa o padrão
    data_inicio = request.GET.get('data_inicio') or str_inicio_mes
    data_fim = request.GET.get('data_fim') or str_hoje

    empresa = request.GET.get('empresa')
    if empresa == '':
        empresa = None

    # Formatação para exibição no template
    try:
        display_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        display_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        display_inicio = data_inicio
        display_fim = data_fim

    # Configura o formulário
    form = GraficoFilterForm(initial={
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'empresa': empresa
    })

    # ---------------------------------------------------------
    # 2. CARGA DE DADOS OTIMIZADA (DataFrames Únicos)
    # ---------------------------------------------------------

    # --- A. Carregar Dados de OS (ConsultaOs) ---
    # Filtramos por data diretamente no banco para trazer apenas o necessário (Performance)
    filtros_os = {
        'abertura__gte': data_inicio,
        'abertura__lte': f"{data_fim} 23:59:59"  # Garante o dia todo
    }
    if empresa:
        filtros_os['empresa'] = empresa

    # Selecionamos apenas as colunas usadas nos gráficos para economizar memória
    cols_os = [
        'os', 'tag', 'local_api', 'empresa', 'abertura', 'fechamento',
        'data_atendimento', 'situacao', 'tipomanutencao', 'causa',
        'prioridade', 'equipamento', 'parada', 'funcionamento'
    ]

    # Executa a query
    qs_os = ConsultaOs.objects.filter(**filtros_os).values(*cols_os)
    df_os = pd.DataFrame(list(qs_os))

    # Pré-processamento Global de Datas (Faz apenas 1 vez para todos os gráficos)
    if not df_os.empty:
        cols_data_os = ['abertura', 'fechamento', 'data_atendimento', 'parada', 'funcionamento']
        for col in cols_data_os:
            # errors='coerce' transforma erros em NaT (Not a Time)
            df_os[col] = pd.to_datetime(df_os[col], errors='coerce')

    # --- B. Carregar Dados de Equipamentos (ConsultaEquipamentos) ---
    filtros_equip = {}
    if empresa:
        filtros_equip['empresa'] = empresa

    # Colunas necessárias
    cols_equip = ['empresa', 'tag', 'familia', 'instalacao', 'cadastro', 'garantia']

    qs_equip = ConsultaEquipamentos.objects.filter(**filtros_equip).values(*cols_equip)
    df_equip = pd.DataFrame(list(qs_equip))

    # Pré-processamento Equipamentos
    if not df_equip.empty:
        df_equip['instalacao'] = pd.to_datetime(df_equip['instalacao'], errors='coerce')
        df_equip['cadastro'] = pd.to_datetime(df_equip['cadastro'], errors='coerce')

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS INDICADORES (Passando os DataFrames)
    # ---------------------------------------------------------

    # 1. Tempo Médio de Atendimento
    labels_atendimento, data_atendimento = get_tempo_medio_atendimento_por_unidade(df_os)

    # 2. Dispersão Reparo x Atendimento
    dados_scatter = get_dispersao_reparo_atendimento(df_os)

    # 3. Tempo Médio de Reparo
    labels_reparo, data_reparo = get_tempo_medio_reparo_por_unidade(df_os)

    # 4. Taxa de Cumprimento
    labels_taxa_cumprimento_medio, data_taxa_cumprimento_medio, qtd_fechada, total_os = get_taxa_cumprimento_por_unidade(df_os)

    taxa_cumprimento_metadados = []
    if labels_taxa_cumprimento_medio:
        for fechada, total in zip(qtd_fechada, total_os):
            taxa_cumprimento_metadados.append({'fechada': fechada, 'total': total})

    # 5. OS por Tipo
    labels_tipo_manutencao_os, data_tipo_manutencao_os = get_qtde_os_por_tipo_manutencao(df_os)

    # 6. Planejadas Realizadas
    labels_qtde_os_planejadas_realizadas, data_qtde_os_planejadas_realizadas = get_qtde_os_planejadas_realizadas(df_os)

    # 7. Planejadas Não Realizadas (Pendentes)
    labels_qtde_os_planejadas_n_realizadas, data_qtde_os_planejadas_n_realizadas = get_qtde_os_planejadas_n_realizadas(df_os)

    # 8. Taxa Conclusão Planejamento
    labels_os_taxa_conclusao_planejamento, data_os_taxa_conclusao_planejamento, qtde_os_taxa_conclusao_planejamento, total_os_taxa_conclusao_planejamento = get_os_taxa_conclusao_planejamento(df_os)

    plan_taxa_metadados = []
    if labels_os_taxa_conclusao_planejamento:
        for qtde_fechada, total in zip(qtde_os_taxa_conclusao_planejamento, total_os_taxa_conclusao_planejamento):
            plan_taxa_metadados.append({'fechada': qtde_fechada, 'total': total})

    # 9. Disponibilidade Geral (Usa OS para estimar inventário ativo no período)
    labels_disponibilidade_equipamentos, data_disponibilidade_equipamentos = get_taxa_disponibilidade_equipamentos(df_os)

    # 10. Qtd Equipamentos (Usa Tabela Equipamentos)
    labels_equipamentos_unidade, data_equipamentos_unidade = get_qtde_equipamentos_por_unidade(df_equip)

    # 11. Idade Média por Unidade
    labels_idade_equipamentos_unidade, data_idade_equipamentos_unidade = get_idade_media_equipamentos_por_unidade(df_equip)

    # 12. Idade Média por Família
    labels_idade_media_equipamentos_familia, data_idade_media_equipamentos_familia = get_idade_media_equipamentos_por_familia(df_equip)

    # 13. Reparo Crítico (OS + Equip)
    labels_reparo_tempo_critico, data_reparo_tempo_critico = get_maiores_tempos_reparo_criticos_por_familia(df_os, df_equip)

    # 14. Principais Causas
    labels_principais_causas_corretivas, data_principais_causas_corretivas = get_principais_causas_corretivas(df_os)

    # 15. Parada Crítica (OS + Equip)
    labels_maiores_tempos_parada_criticos_por_familia, data_maiores_tempos_parada_criticos_por_familia = get_maiores_tempos_parada_criticos_por_familia(df_os, df_equip)

    # 16. Mediana Parada
    labels_tempo_mediano_parada_criticos_por_unidade, data_tempo_mediano_parada_criticos_por_unidade = get_tempo_mediano_parada_criticos_por_unidade(df_os)

    # 17. Heatmap Indisponibilidade
    pivot_indisponibilidade_equipamentos_criticos = get_matriz_indisponibilidade_criticos(df_os)

    # 18. Disponibilidade Críticos
    labels_taxa_disponibilidade_equipamentos_criticos, data_taxa_disponibilidade_equipamentos_criticos = get_taxa_disponibilidade_equipamentos_criticos(df_os)

    # 19. Qtd Críticos (OS + Equip)
    labels_equipamentos_criticos_por_unidade, data_equipamentos_criticos_por_unidade = get_qtde_equipamentos_criticos_por_unidade(df_os, df_equip)

    # 20. Primeiro Atendimento Crítico
    labels_primeiro_atendimento_equipamento_critico, data_primeiro_atendimento_equipamento_critico = get_tempo_primeiro_atendimento_critico(df_os)

    # ---------------------------------------------------------
    # 4. Contexto do Template
    # ---------------------------------------------------------
    context = {
        'form': form,
        'display_inicio': display_inicio,
        'display_fim': display_fim,

        # Gráficos
        'labels_atendimento': labels_atendimento,
        'data_atendimento': data_atendimento,
        'dados_scatter': dados_scatter,
        'labels_reparo': labels_reparo,
        'data_reparo': data_reparo,
        'labels_taxa_cumprimento_medio': labels_taxa_cumprimento_medio,
        'data_taxa_cumprimento_medio': data_taxa_cumprimento_medio,
        'taxa_cumprimento_metadados': taxa_cumprimento_metadados,
        'labels_tipo_manutencao_os': labels_tipo_manutencao_os,
        'data_tipo_manutencao_os': data_tipo_manutencao_os,
        'labels_qtde_os_planejadas_realizadas': labels_qtde_os_planejadas_realizadas,
        'data_qtde_os_planejadas_realizadas': data_qtde_os_planejadas_realizadas,
        'labels_qtde_os_planejadas_n_realizadas': labels_qtde_os_planejadas_n_realizadas,
        'data_qtde_os_planejadas_n_realizadas': data_qtde_os_planejadas_n_realizadas,
        'labels_os_taxa_conclusao_planejamento': labels_os_taxa_conclusao_planejamento,
        'data_os_taxa_conclusao_planejamento': data_os_taxa_conclusao_planejamento,
        'plan_taxa_metadados': plan_taxa_metadados,
        'labels_disponibilidade_equipamentos': labels_disponibilidade_equipamentos,
        'data_disponibilidade_equipamentos': data_disponibilidade_equipamentos,
        'labels_equipamentos_unidade': labels_equipamentos_unidade,
        'data_equipamentos_unidade': data_equipamentos_unidade,
        'labels_idade_equipamentos_unidade': labels_idade_equipamentos_unidade,
        'data_idade_equipamentos_unidade': data_idade_equipamentos_unidade,
        'labels_idade_media_equipamentos_familia': labels_idade_media_equipamentos_familia,
        'data_idade_media_equipamentos_familia': data_idade_media_equipamentos_familia,
        'labels_reparo_tempo_critico': labels_reparo_tempo_critico,
        'data_reparo_tempo_critico': data_reparo_tempo_critico,
        'labels_principais_causas_corretivas': labels_principais_causas_corretivas,
        'data_principais_causas_corretivas': data_principais_causas_corretivas,
        'labels_maiores_tempos_parada_criticos_por_familia': labels_maiores_tempos_parada_criticos_por_familia,
        'data_maiores_tempos_parada_criticos_por_familia': data_maiores_tempos_parada_criticos_por_familia,
        'labels_tempo_mediano_parada_criticos_por_unidade': labels_tempo_mediano_parada_criticos_por_unidade,
        'data_tempo_mediano_parada_criticos_por_unidade': data_tempo_mediano_parada_criticos_por_unidade,
        'pivot_indisponibilidade_equipamentos_criticos': pivot_indisponibilidade_equipamentos_criticos,
        'labels_taxa_disponibilidade_equipamentos_criticos': labels_taxa_disponibilidade_equipamentos_criticos,
        'data_taxa_disponibilidade_equipamentos_criticos': data_taxa_disponibilidade_equipamentos_criticos,
        'labels_equipamentos_criticos_por_unidade': labels_equipamentos_criticos_por_unidade,
        'data_equipamentos_criticos_por_unidade': data_equipamentos_criticos_por_unidade,
        'labels_primeiro_atendimento_equipamento_critico': labels_primeiro_atendimento_equipamento_critico,
        'data_primeiro_atendimento_equipamento_critico': data_primeiro_atendimento_equipamento_critico,
    }

    return render(request, 'engenharia/graficos.html', context)


def engenharia_clinica_indicadores(request):
    # ---------------------------------------------------------
    # 1. Configuração de Datas e Filtros Iniciais
    # ---------------------------------------------------------
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)

    str_hoje = hoje.strftime('%Y-%m-%d')
    str_inicio_mes = inicio_mes.strftime('%Y-%m-%d')

    # Pega da URL ou usa o padrão
    data_inicio = request.GET.get('data_inicio') or str_inicio_mes
    data_fim = request.GET.get('data_fim') or str_hoje

    empresa = request.GET.get('empresa')
    if empresa == '':
        empresa = None

    # Formatação para exibição no template
    try:
        display_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        display_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        display_inicio = data_inicio
        display_fim = data_fim

    # Configura o formulário
    form = GraficoFilterForm(initial={
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'empresa': empresa
    })

    # ---------------------------------------------------------
    # 2. CARGA DE DADOS OTIMIZADA (DataFrames Únicos)
    # ---------------------------------------------------------

    # --- A. Carregar Dados de OS (ConsultaOs) ---
    # Filtramos por data diretamente no banco para trazer apenas o necessário (Performance)
    filtros_os = {}
    if empresa:
        filtros_os['empresa'] = empresa

    # Selecionamos apenas as colunas usadas nos gráficos para economizar memória
    cols_os = [
        'os', 'tag', 'local_api', 'empresa', 'abertura', 'fechamento',
        'data_atendimento', 'situacao', 'tipomanutencao', 'causa',
        'prioridade', 'equipamento', 'parada', 'funcionamento', 'ocorrencia',
        'data_chamado'
    ]

    # Executa a query
    qs_os = ConsultaOs.objects.filter(**filtros_os).values(*cols_os)
    df_os = pd.DataFrame(list(qs_os))

    # Pré-processamento Global de Datas (Faz apenas 1 vez para todos os gráficos)
    if not df_os.empty:
        cols_data_os = ['abertura', 'fechamento', 'data_atendimento', 'parada', 'funcionamento']
        for col in cols_data_os:
            # errors='coerce' transforma erros em NaT (Not a Time)
            df_os[col] = pd.to_datetime(df_os[col], errors='coerce')

    # --- B. Carregar Dados de Equipamentos (ConsultaEquipamentos) ---
    filtros_equip = {
        'cadastro__gte': data_inicio,
        'cadastro__lte': f"{data_fim} 23:59:59"
    }
    if empresa:
        filtros_equip['empresa'] = empresa

    # Colunas necessárias
    cols_equip = ['empresa', 'tag', 'familia', 'instalacao', 'cadastro', 'garantia']

    qs_equip = ConsultaEquipamentos.objects.filter(**filtros_equip).values(*cols_equip)
    df_equip = pd.DataFrame(list(qs_equip))

    # Pré-processamento Equipamentos
    if not df_equip.empty:
        df_equip['instalacao'] = pd.to_datetime(df_equip['instalacao'], errors='coerce')
        df_equip['cadastro'] = pd.to_datetime(df_equip['cadastro'], errors='coerce')

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS INDICADORES (Passando os DataFrames)
    # ---------------------------------------------------------
    total_equipamentos_cadastrados = get_total_equipamentos_cadastrados(df_equip)
    total_os_corretiva = get_total_os_corretivas(df_os)
    maiores_causas_corretivas = get_maiores_causas_corretivas(df_os, data_inicio, data_fim)
    kpi_mtbf = get_mtbf_medio_kpi(df_equip)
    kpi_mttr = get_mttr_kpi(df_os, data_inicio, data_fim)
    kpi_tma = get_tempo_medio_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)
    kpi_tma_mediana = get_tempo_mediano_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)

    context = {
        'form': form,
        'display_inicio': display_inicio,
        'display_fim': display_fim,

        # Indicadores
        'total_equipamentos_cadastrados': total_equipamentos_cadastrados,
        'total_os_corretiva': total_os_corretiva,
        'maiores_causas_corretivas': maiores_causas_corretivas,
        'kpi_mtbf': kpi_mtbf,
        'kpi_mttr': kpi_mttr,
        'kpi_tma': kpi_tma,
        'kpi_tma_mediana': kpi_tma_mediana,

    }
    return render(request, 'engenharia/indicadores.html', context)
