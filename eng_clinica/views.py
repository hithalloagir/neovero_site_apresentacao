import pandas as pd
from django.shortcuts import render
from datetime import datetime
from .forms import GraficoFilterForm
from .models import ConsultaOs, ConsultaEquipamentos
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

    t_db = time.time()

    # --- A. Carregar Dados de OS (ConsultaOs) ---
    # Filtramos por data diretamente no banco para trazer apenas o necessário (Performance)
    filtros_os = {}
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

    # --- LOG DB ---
    print(f"⏱️ [DB Load - Gráficos] Carregar Dados: {time.time() - t_db:.4f} segundos")
    print(f"   -> Linhas OS: {len(df_os)}")
    print(f"   -> Linhas Equip: {len(df_equip)}")

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS INDICADORES (Passando os DataFrames)
    # ---------------------------------------------------------
    t_calc = time.time()

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
    taxa_cumprimento_metadados = []
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
    plan_taxa_metadados = []
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
        df_os=df_os,
        df_equip=df_equip,
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

    # --- LOG CALC ---
    print(f"⏱️ [Cálculo - Gráficos] Processar funções Python: {time.time() - t_calc:.4f} segundos")
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

    # --- LOG FINAL ---
    tempo_total = time.time() - start_total
    print(f"🚀 [TOTAL - Gráficos] Tempo total da View: {tempo_total:.4f} segundos")
    print("-" * 50)

    return render(request, 'engenharia/graficos.html', context)


def engenharia_clinica_indicadores(request):
    # --- INÍCIO DO CRONÔMETRO GERAL (INDICADORES) ---
    start_total = time.time()
    print("-" * 50)
    print("📈 INICIANDO VIEW DE INDICADORES")

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

    t_db = time.time()  # Timer DB

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

    # --- LOG DB ---
    print(f"⏱️ [DB Load - Indicadores] Carregar Dados: {time.time() - t_db:.4f} segundos")
    print(f"   -> Linhas OS: {len(df_os)}")
    print(f"   -> Linhas Equip: {len(df_equip)}")

    # ---------------------------------------------------------
    # 3. GERAÇÃO DOS INDICADORES (Passando os DataFrames)
    # ---------------------------------------------------------
    t_calc = time.time()  # Timer Calc

    total_equipamentos_cadastrados = get_total_equipamentos_cadastrados(df_equip, data_inicio, data_fim)
    total_os_corretiva = get_total_os_corretivas(df_os, data_inicio, data_fim)
    maiores_causas_corretivas = get_maiores_causas_corretivas(df_os, data_inicio, data_fim)

    # MTBF (Geralmente é sobre o inventário ATUAL/TOTAL, então não costuma ter filtro de data no df_equip, a menos que queira MTBF só de máquinas novas)
    kpi_mtbf = get_mtbf_medio_kpi(df_equip)

    kpi_mttr = get_mttr_kpi(df_os, data_inicio, data_fim)
    kpi_reparos_imediato = get_qtde_reparos_imediato_kpi(df_os, data_inicio, data_fim)
    kpi_tma = get_tempo_medio_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)
    kpi_tma_mediana = get_tempo_mediano_primeiro_atendimento_kpi(df_os, data_inicio, data_fim)
    kpi_tma_critico = get_tempo_medio_primeiro_atendimento_critico_kpi(df_os, data_inicio, data_fim)
    kpi_tma_critico_mediana = get_tempo_mediano_primeiro_atendimento_critico_kpi(df_os, data_inicio, data_fim)
    kpi_tma_equipamento_critico_parado = get_tempo_medio_equipamento_critico_parado_kpi(df_os, data_inicio, data_fim)
    kpi_tma_equipamento_critico_parado_mediana = get_tempo_mediano_equipamento_critico_parado_kpi(df_os, data_inicio, data_fim)
    kpi_taxa_disponibilidade = get_taxa_disponibilidade_kpi(df_os, df_equip, data_inicio, data_fim)
    kpi_taxa_disponibilidade_criticos = get_taxa_disponibilidade_criticos_kpi(df_os, df_equip, data_inicio, data_fim)
    kpi_equip_indisponiveis = get_qtde_equipamentos_indisponiveis_kpi(df_os, data_inicio, data_fim)
    kpi_equip_criticos_indisponiveis = get_qtde_equipamentos_criticos_indisponiveis_kpi(df_os, data_inicio, data_fim)
    kpi_resolucao_corretivas = get_taxa_resolucao_corretivas_periodo_kpi(df_os, data_inicio, data_fim)
    kpi_pendencias_corretiva = get_pendencias_corretiva_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_preventiva = get_cumprimento_preventiva_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_calibracao = get_cumprimento_calibracao_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_treinamento = get_cumprimento_treinamento_kpi(df_os, data_inicio, data_fim)
    kpi_cumprimento_tse = get_cumprimento_tse_kpi(df_os, data_inicio, data_fim)
    tabela_corretivas_familia = get_os_corretivas_ultimos_3_anos_por_familia(df_os, df_equip)

    # --- LOG CALC ---
    print(f"⏱️ [Cálculo - Indicadores] Processar funções Python: {time.time() - t_calc:.4f} segundos")

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
        'kpi_reparos_imediato': kpi_reparos_imediato,
        'kpi_tma': kpi_tma,
        'kpi_tma_mediana': kpi_tma_mediana,
        'kpi_tma_critico': kpi_tma_critico,
        'kpi_tma_critico_mediana': kpi_tma_critico_mediana,
        'kpi_tma_equipamento_critico_parado': kpi_tma_equipamento_critico_parado,
        'kpi_tma_equipamento_critico_parado_mediana': kpi_tma_equipamento_critico_parado_mediana,
        'kpi_taxa_disponibilidade': kpi_taxa_disponibilidade,
        'kpi_taxa_disponibilidade_criticos': kpi_taxa_disponibilidade_criticos,
        'kpi_equip_indisponiveis': kpi_equip_indisponiveis,
        'kpi_equip_criticos_indisponiveis': kpi_equip_criticos_indisponiveis,
        'kpi_resolucao_corretivas': kpi_resolucao_corretivas,
        'kpi_pendencias_corretiva': kpi_pendencias_corretiva,
        'kpi_cumprimento_preventiva': kpi_cumprimento_preventiva,
        'kpi_cumprimento_calibracao': kpi_cumprimento_calibracao,
        'kpi_cumprimento_treinamento': kpi_cumprimento_treinamento,
        'kpi_cumprimento_tse': kpi_cumprimento_tse,
        'tabela_corretivas_familia': tabela_corretivas_familia,
    }

    # --- LOG FINAL ---
    tempo_total = time.time() - start_total
    print(f"🚀 [TOTAL - Indicadores] Tempo total da View: {tempo_total:.4f} segundos")
    print("-" * 50)
    return render(request, 'engenharia/indicadores.html', context)
