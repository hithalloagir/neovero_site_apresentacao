import pandas as pd
from django.shortcuts import render
from datetime import datetime
from .forms import GraficoFilterForm
from .models import ConsultaOsNew, ConsultaEquipamentos
import time

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
    get_qtde_reparos_imediato_kpi,
    get_tempo_medio_primeiro_atendimento_kpi,
    get_tempo_mediano_primeiro_atendimento_kpi,
    get_tempo_medio_primeiro_atendimento_critico_kpi,
    get_tempo_mediano_primeiro_atendimento_critico_kpi,
    get_tempo_medio_equipamento_critico_parado_kpi,
    get_tempo_mediano_equipamento_critico_parado_kpi,
    get_taxa_disponibilidade_kpi,
    get_taxa_disponibilidade_criticos_kpi,
    get_qtde_equipamentos_indisponiveis_kpi,
    get_qtde_equipamentos_criticos_indisponiveis_kpi,
    get_taxa_resolucao_corretivas_periodo_kpi,
    get_pendencias_corretiva_kpi,
    get_cumprimento_preventiva_kpi,
    get_cumprimento_calibracao_kpi,
    get_cumprimento_treinamento_kpi,
    get_cumprimento_tse_kpi,
    get_os_corretivas_ultimos_3_anos_por_familia,
)


def home(request):
    return render(request, 'engenharia/home.html')


def engenharia_clinica_graficos(request):
    # --- INÍCIO DO CRONÔMETRO GERAL ---
    start_total = time.time()

    # ---------------------------------------------------------
    # 1. Configuração de Datas e Filtros Iniciais
    # ---------------------------------------------------------
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)

    str_hoje = hoje.strftime('%Y-%m-%d')
    str_inicio_mes = inicio_mes.strftime('%Y-%m-%d')

    data_inicio = request.GET.get('data_inicio') or str_inicio_mes
    data_fim = request.GET.get('data_fim') or str_hoje
    empresa = request.GET.get('empresa')
    if empresa == '':
        empresa = None

    # Formatação visual
    try:
        display_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        display_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        display_inicio, display_fim = data_inicio, data_fim

    form = GraficoFilterForm(initial={'data_inicio': data_inicio, 'data_fim': data_fim, 'empresa': empresa})

    # ---------------------------------------------------------
    # 2. CARGA DE DADOS CENTRALIZADA E OTIMIZADA
    # ---------------------------------------------------------
    t_db = time.time()

    # --- A. Carregar EQUIPAMENTOS e aplicar filtro "Equipamento Médico" ---
    filtros_equip = {}
    if empresa:
        filtros_equip['empresa'] = empresa

    cols_equip = ['empresa', 'tag', 'familia', 'instalacao', 'cadastro', 'garantia', 'tipoequipamento']
    qs_equip = ConsultaEquipamentos.objects.filter(**filtros_equip).values(*cols_equip)
    df_equip = pd.DataFrame(list(qs_equip))

    tags_validas = []

    if not df_equip.empty:
        # 1. Normaliza texto
        df_equip['tipoequipamento'] = df_equip['tipoequipamento'].astype(str).str.strip().str.upper()

        # 2. FILTRO GLOBAL: Regex para pegar "Equipamento Médico" (com ou sem acento/erro)
        # Regex: EQUIPAMENTO + espaços + M + qualquer coisa + DICO
        df_equip = df_equip[
            df_equip['tipoequipamento'].str.contains(r'EQUIPAMENTO\s+M.*DICO', regex=True, na=False)
        ]

        # Guardamos as tags válidas para filtrar as OSs depois
        tags_validas = df_equip['tag'].unique().tolist()

        # Pré-processamento de datas do Equipamento
        df_equip['instalacao'] = pd.to_datetime(df_equip['instalacao'], errors='coerce')
        df_equip['cadastro'] = pd.to_datetime(df_equip['cadastro'], errors='coerce')

    # --- B. Carregar OS (Filtrando apenas as Tags dos Equipamentos Médicos) ---
    filtros_os = {}
    if empresa:
        filtros_os['empresa'] = empresa

    # OTIMIZAÇÃO CRÍTICA: Só busca OS se a tag estiver na lista de equipamentos médicos filtrados
    if tags_validas:
        filtros_os['tag__in'] = tags_validas

    cols_os = [
        'os', 'tag', 'local_api', 'empresa', 'abertura', 'fechamento',
        'data_atendimento', 'situacao', 'tipomanutencao', 'causa',
        'prioridade', 'equipamento', 'parada', 'funcionamento'
    ]

    # Se não tiver equipamentos médicos, nem busca OS (retorna vazio)
    if not tags_validas:
        df_os = pd.DataFrame(columns=cols_os)
    else:
        qs_os = ConsultaOsNew.objects.filter(**filtros_os).values(*cols_os)
        df_os = pd.DataFrame(list(qs_os))

    # Pré-processamento Global de Datas da OS
    if not df_os.empty:
        cols_data_os = ['abertura', 'fechamento', 'data_atendimento', 'parada', 'funcionamento']
        for col in cols_data_os:
            df_os[col] = pd.to_datetime(df_os[col], errors='coerce')

        # Garantia final: Filtra o DF para ter certeza que só tem as tags certas
        # (Caso o banco tenha trazido algo a mais por case sensitivity)
        df_os['tag'] = df_os['tag'].astype(str).str.strip().str.upper()
        # df_os = df_os[df_os['tag'].isin([t.strip().upper() for t in tags_validas])] # Opcional se o tag__in funcionar bem

    print(f"⏱️ [DB Load] Dados Filtrados (Só Médico): {time.time() - t_db:.4f}s | OS: {len(df_os)} | Equip: {len(df_equip)}")

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS GRÁFICOS (Passando os DFs prontos)
    # ---------------------------------------------------------
    t_calc = time.time()

    # IMPORTANTE: Agora passamos 'df_os' e/ou 'df_equip' para TODAS as funções

    labels_atendimento, data_atendimento = get_tempo_medio_atendimento_por_unidade(
        df_os, data_inicio, data_fim, empresa
    )

    # dados_scatter = get_dispersao_reparo_atendimento(
    #     df_os, data_inicio, data_fim, empresa
    # )

    labels_reparo, data_reparo = get_tempo_medio_reparo_por_unidade(
        df_os, data_inicio, data_fim, empresa
    )

    labels_taxa_cumprimento_medio, data_taxa_cumprimento_medio, qtd_fechada, total_os = get_taxa_cumprimento_por_unidade(
        df_os, data_inicio, data_fim, empresa
    )

    taxa_cumprimento_metadados = [{'fechada': f, 'total': t} for f, t in zip(qtd_fechada, total_os)]

    labels_tipo_manutencao_os, data_tipo_manutencao_os = get_qtde_os_por_tipo_manutencao(
        df_os, data_inicio, data_fim, empresa
    )

    labels_qtde_os_planejadas_realizadas, data_qtde_os_planejadas_realizadas = get_qtde_os_planejadas_realizadas(
        df_os, data_inicio, data_fim, empresa
    )

    labels_qtde_os_planejadas_n_realizadas, data_qtde_os_planejadas_n_realizadas = get_qtde_os_planejadas_n_realizadas(
        df_os, data_inicio, data_fim, empresa
    )

    labels_os_taxa_conclusao_planejamento, data_os_taxa_conclusao_planejamento, qtde_plan, total_plan = get_os_taxa_conclusao_planejamento(
        df_os, data_inicio, data_fim, empresa
    )
    plan_taxa_metadados = [{'fechada': f, 'total': t} for f, t in zip(qtde_plan, total_plan)]

    # Disponibilidade precisa de OS e Equipamentos
    labels_disponibilidade_equipamentos, data_disponibilidade_equipamentos = get_taxa_disponibilidade_equipamentos(
        df_os, df_equip, data_inicio, data_fim, empresa
    )

    # labels_equipamentos_unidade, data_equipamentos_unidade = get_qtde_equipamentos_por_unidade(
    #     df_equip, data_inicio, data_fim, empresa
    # )

    labels_idade_equipamentos_unidade, data_idade_equipamentos_unidade = get_idade_media_equipamentos_por_unidade(
        df_equip, data_inicio, data_fim, empresa
    )

    labels_idade_media_equipamentos_familia, data_idade_media_equipamentos_familia = get_idade_media_equipamentos_por_familia(
        df_equip, data_inicio, data_fim, empresa
    )

    labels_reparo_tempo_critico, data_reparo_tempo_critico = get_maiores_tempos_reparo_criticos_por_familia(
        df_os, df_equip, data_inicio, data_fim, empresa
    )

    labels_principais_causas_corretivas, data_principais_causas_corretivas = get_principais_causas_corretivas(
        df_os, data_inicio, data_fim, empresa
    )

    labels_maiores_tempos_parada_criticos_por_familia, data_maiores_tempos_parada_criticos_por_familia = get_maiores_tempos_parada_criticos_por_familia(
        df_os, df_equip, data_inicio, data_fim, empresa
    )

    labels_tempo_mediano_parada_criticos_por_unidade, data_tempo_mediano_parada_criticos_por_unidade = get_tempo_mediano_parada_criticos_por_unidade(
        df_os, data_inicio, data_fim, empresa
    )

    pivot_indisponibilidade_equipamentos_criticos = get_matriz_indisponibilidade_criticos(
        df_os, data_inicio, data_fim, empresa
    )

    labels_taxa_disponibilidade_equipamentos_criticos, data_taxa_disponibilidade_equipamentos_criticos = get_taxa_disponibilidade_equipamentos_criticos(
        df_os, df_equip, data_inicio, data_fim, empresa
    )

    labels_equipamentos_criticos_por_unidade, data_equipamentos_criticos_por_unidade = get_qtde_equipamentos_criticos_por_unidade(
        df_os, df_equip, data_inicio, data_fim, empresa
    )

    labels_primeiro_atendimento_equipamento_critico, data_primeiro_atendimento_equipamento_critico = get_tempo_primeiro_atendimento_critico(
        df_os, data_inicio, data_fim, empresa
    )

    print(f"⏱️ [Cálculo] Processamento Python: {time.time() - t_calc:.4f}s")

    # ---------------------------------------------------------
    # 4. Contexto do Template
    # ---------------------------------------------------------
    context = {
        'form': form,
        'display_inicio': display_inicio,
        'display_fim': display_fim,
        # ... (Mantém todas as variáveis de contexto exatamente como estavam) ...
        'labels_atendimento': labels_atendimento,
        'data_atendimento': data_atendimento,
        # 'dados_scatter': dados_scatter,
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
        # 'labels_equipamentos_unidade': labels_equipamentos_unidade,
        # 'data_equipamentos_unidade': data_equipamentos_unidade,
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

    print(f"🚀 [TOTAL] Tempo Total: {time.time() - start_total:.4f}s")
    return render(request, 'engenharia/graficos.html', context)


def engenharia_clinica_indicadores(request):
    # --- INÍCIO DO CRONÔMETRO GERAL (INDICADORES) ---
    start_total = time.time()
    print("-" * 50)
    print("📈 INICIANDO VIEW DE INDICADORES (OTIMIZADA)")

    # ---------------------------------------------------------
    # 1. Configuração de Datas e Filtros Iniciais
    # ---------------------------------------------------------
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)

    str_hoje = hoje.strftime('%Y-%m-%d')
    str_inicio_mes = inicio_mes.strftime('%Y-%m-%d')

    data_inicio = request.GET.get('data_inicio') or str_inicio_mes
    data_fim = request.GET.get('data_fim') or str_hoje

    empresa = request.GET.get('empresa')
    if empresa == '':
        empresa = None

    try:
        display_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        display_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        display_inicio, display_fim = data_inicio, data_fim

    form = GraficoFilterForm(initial={
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'empresa': empresa
    })

    # ---------------------------------------------------------
    # 2. CARGA DE DADOS OTIMIZADA (DataFrames Únicos)
    # ---------------------------------------------------------
    t_db = time.time()

    # --- A. Carregar EQUIPAMENTOS e aplicar filtro "Equipamento Médico" ---
    filtros_equip = {}
    if empresa:
        filtros_equip['empresa'] = empresa

    # Adicionamos 'tipoequipamento' para o filtro REGEX
    cols_equip = ['empresa', 'tag', 'familia', 'instalacao', 'cadastro', 'garantia', 'tipoequipamento']

    qs_equip = ConsultaEquipamentos.objects.filter(**filtros_equip).values(*cols_equip)
    df_equip = pd.DataFrame(list(qs_equip))

    tags_validas = []

    if not df_equip.empty:
        # 1. Normaliza texto
        df_equip['tipoequipamento'] = df_equip['tipoequipamento'].astype(str).str.strip().str.upper()

        # 2. FILTRO GLOBAL: Regex para pegar "Equipamento Médico" (blinda contra erros de acento)
        df_equip = df_equip[
            df_equip['tipoequipamento'].str.contains(r'EQUIPAMENTO\s+M.*DICO', regex=True, na=False)
        ]

        # Pré-processamento de datas do Equipamento
        df_equip['instalacao'] = pd.to_datetime(df_equip['instalacao'], errors='coerce')
        df_equip['cadastro'] = pd.to_datetime(df_equip['cadastro'], errors='coerce')

        tags_validas = df_equip['tag'].unique().tolist()

    # --- B. Carregar Dados de OS (Filtrando apenas Tags Médicas) ---
    filtros_os = {}
    if empresa:
        filtros_os['empresa'] = empresa

    # OTIMIZAÇÃO: Só busca OS se a tag estiver na lista filtrada
    if tags_validas:
        filtros_os['tag__in'] = tags_validas

    cols_os = [
        'os', 'tag', 'local_api', 'empresa', 'abertura', 'fechamento',
        'data_atendimento', 'situacao', 'tipomanutencao', 'causa',
        'prioridade', 'equipamento', 'parada', 'funcionamento', 'ocorrencia',
        'data_chamado'
    ]

    if not tags_validas:
        df_os = pd.DataFrame(columns=cols_os)
    else:
        qs_os = ConsultaOsNew.objects.filter(**filtros_os).values(*cols_os)
        df_os = pd.DataFrame(list(qs_os))

    # Pré-processamento Global de Datas da OS
    if not df_os.empty:
        cols_data_os = ['abertura', 'fechamento', 'data_atendimento', 'parada', 'funcionamento', 'data_chamado']
        for col in cols_data_os:
            if col in df_os.columns:
                df_os[col] = pd.to_datetime(df_os[col], errors='coerce')

        # Garantia final de filtro no Pandas
        df_os['tag'] = df_os['tag'].astype(str).str.strip().str.upper()

    print(f"⏱️ [DB Load - Indicadores] Dados Filtrados (Só Médico): {time.time() - t_db:.4f}s")
    print(f"   -> Linhas OS: {len(df_os)}")
    print(f"   -> Linhas Equip: {len(df_equip)}")

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS INDICADORES (Passando os DataFrames)
    # ---------------------------------------------------------
    t_calc = time.time()

    total_equipamentos_cadastrados = get_total_equipamentos_cadastrados(df_equip, data_inicio, data_fim)
    taxa_corretiva, fechadas_corretiva, abertas_corretiva = get_total_os_corretivas(df_os, data_inicio, data_fim)
    maiores_causas_corretivas = get_maiores_causas_corretivas(df_os, data_inicio, data_fim)

    # ATENÇÃO: MTBF agora recebe df_os também para evitar query no banco
    kpi_mtbf = get_mtbf_medio_kpi(df_equip, df_os)

    kpi_mttr = get_mttr_kpi(df_os, data_inicio, data_fim)
    kpi_reparos_imediato = get_qtde_reparos_imediato_kpi(df_os, data_inicio, data_fim)
    kpi_tma = get_tempo_medio_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)
    # kpi_tma_mediana = get_tempo_mediano_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)
    kpi_tma_critico = get_tempo_medio_primeiro_atendimento_critico_kpi(df_os, data_inicio, data_fim)
    # kpi_tma_critico_mediana = get_tempo_mediano_primeiro_atendimento_critico_kpi(df_os, data_inicio, data_fim)
    # kpi_tma_equipamento_critico_parado = get_tempo_medio_equipamento_critico_parado_kpi(df_os, data_inicio, data_fim)
    # kpi_tma_equipamento_critico_parado_mediana = get_tempo_mediano_equipamento_critico_parado_kpi(df_os, data_inicio, data_fim)
    kpi_taxa_disponibilidade = get_taxa_disponibilidade_kpi(df_os, df_equip, data_inicio, data_fim)
    kpi_taxa_disponibilidade_criticos = get_taxa_disponibilidade_criticos_kpi(df_os, df_equip, data_inicio, data_fim)
    # kpi_equip_indisponiveis = get_qtde_equipamentos_indisponiveis_kpi(df_os, data_inicio, data_fim)
    # kpi_equip_criticos_indisponiveis = get_qtde_equipamentos_criticos_indisponiveis_kpi(df_os, data_inicio, data_fim)
    # kpi_resolucao_corretivas = get_taxa_resolucao_corretivas_periodo_kpi(df_os, data_inicio, data_fim)
    # kpi_pendencias_corretiva = get_pendencias_corretiva_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_preventiva = get_cumprimento_preventiva_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_calibracao = get_cumprimento_calibracao_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_treinamento = get_cumprimento_treinamento_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_tse = get_cumprimento_tse_kpi(df_os, data_inicio, data_fim)
    tabela_corretivas_familia = get_os_corretivas_ultimos_3_anos_por_familia(df_os, df_equip)

    print(f"⏱️ [Cálculo - Indicadores] Processar funções Python: {time.time() - t_calc:.4f} segundos")

    context = {
        'form': form,
        'display_inicio': display_inicio,
        'display_fim': display_fim,
        # Indicadores
        'total_equipamentos_cadastrados': total_equipamentos_cadastrados,
        'taxa_corretiva': taxa_corretiva,
        'fechadas_corretiva': fechadas_corretiva,
        'abertas_corretiva': abertas_corretiva,
        'maiores_causas_corretivas': maiores_causas_corretivas,
        'kpi_mtbf': kpi_mtbf,
        'kpi_mttr': kpi_mttr,
        'kpi_reparos_imediato': kpi_reparos_imediato,
        'kpi_tma': kpi_tma,
        # 'kpi_tma_mediana': kpi_tma_mediana,
        'kpi_tma_critico': kpi_tma_critico,
        # 'kpi_tma_critico_mediana': kpi_tma_critico_mediana,
        # 'kpi_tma_equipamento_critico_parado': kpi_tma_equipamento_critico_parado,
        # 'kpi_tma_equipamento_critico_parado_mediana': kpi_tma_equipamento_critico_parado_mediana,
        'kpi_taxa_disponibilidade': kpi_taxa_disponibilidade,
        'kpi_taxa_disponibilidade_criticos': kpi_taxa_disponibilidade_criticos,
        # 'kpi_equip_indisponiveis': kpi_equip_indisponiveis,
        # 'kpi_equip_criticos_indisponiveis': kpi_equip_criticos_indisponiveis,
        # 'kpi_resolucao_corretivas': kpi_resolucao_corretivas,
        # 'kpi_pendencias_corretiva': kpi_pendencias_corretiva,
        'kpi_cumprimento_preventiva': kpi_cumprimento_preventiva,
        'kpi_cumprimento_calibracao': kpi_cumprimento_calibracao,
        'kpi_cumprimento_treinamento': kpi_cumprimento_treinamento,
        'kpi_cumprimento_tse': kpi_cumprimento_tse,
        'tabela_corretivas_familia': tabela_corretivas_familia,
    }

    tempo_total = time.time() - start_total
    print(f"🚀 [TOTAL - Indicadores] Tempo total da View: {tempo_total:.4f} segundos")
    print("-" * 50)
    return render(request, 'engenharia/indicadores.html', context)
