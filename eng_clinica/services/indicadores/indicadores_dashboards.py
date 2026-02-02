import pandas as pd
import numpy as np
from django.db.models import Count
from ...models import ConsultaOs


def get_total_equipamentos_cadastrados(df_equip):
    """
    Retorna a quantidade de equipamentos cuja data de CADASTRO está no período.
    Usado na tela de Indicadores.
    """
    if df_equip.empty:
        return 0

    # 1. Copia e Deduplica (Tag única)
    # Não precisamos agrupar por empresa, pois queremos o totalzão (ou o total da empresa filtrada)
    df = df_equip.drop_duplicates(subset=['tag'])

    # 2. Retorna a contagem total de linhas
    return df.shape[0]


def get_total_os_corretivas(df_os):
    """
    Retorna o total de OSs CORRETIVAS fechadas no período.
    Regras:
      - Date Range Dimension: fechamento
      - Filter: tipomanutencao = 'CORRETIVA'
      - Filter: MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    if df.empty:
        return 0

    # 3. Filtro de Tipo: Corretivas
    # Normaliza para maiúsculo para garantir
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    if df.empty:
        return 0

    # 4. Filtro: MenosDuplicadas (OS + Tag + Local)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Retorna Contagem
    return df.shape[0]


def get_maiores_causas_corretivas(df_os, data_inicio=None, data_fim=None):
    """
    Retorna o Top 10 Causas de Corretivas (Tabela com Barras).
    Regras:
      - Date Range: abertura
      - Filter: tipomanutencao = 'CORRETIVA'
      - Filter: Exclude situacao in ['ABERTA', 'PENDENTE']
      - Filter: MenosDuplicadas
    """
    if df_os.empty:
        return

    df = df_os.copy()

    # 1. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
        df = df.dropna(subset=['abertura'])

        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]
    else:
        return []

    if df.empty:
        return []

    # 2. Filtro Tipo: Corretiva
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 3. Filtro Situação: Excluir Abertas e Pendentes
    if 'situacao' in df.columns:
        excluir = ['ABERTA', 'PENDENTE']
        df = df[~df['situacao'].str.upper().isin(excluir)]

    if df.empty:
        return []

    # 4. Filtro Duplicatas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Agrupamento e Ranking
    if 'causa' in df.columns:
        # Trata vazios
        df['causa'] = df['causa'].fillna('NÃO INFORMADO').replace('', 'NÃO INFORMADO')

        # Conta e ordena
        counts = df['causa'].value_counts().reset_index()
        counts.columns = ['causa', 'qtd']

        # Calcula % para a barra visual
        total_geral = counts['qtd'].sum()
        counts['percent'] = (counts['qtd'] / total_geral * 100).round(1) if total_geral > 0 else 0

        # Retorna Top 10 como lista de dicionários
        return counts.head(10).to_dict('records')

    return []


def get_mtbf_medio_kpi(df_equip):
    """
    Calcula o MTBF Médio em ANOS.
    """
    if df_equip.empty:
        return 0

    tags = df_equip['tag'].dropna().unique().tolist()
    if not tags:
        return 0

    # Busca falhas (Total histórico)
    qs_falhas = ConsultaOs.objects.filter(
        tag__in=tags,
        tipomanutencao__iexact='CORRETIVA'
    ).values('tag').annotate(qtd=Count('pk'))

    dict_falhas = {x['tag']: x['qtd'] for x in qs_falhas}

    mtbf_values = []
    agora = pd.Timestamp.now()

    for _, row in df_equip.iterrows():
        tag = row['tag']
        data_ref = row['instalacao'] if pd.notnull(row['instalacao']) else row['cadastro']

        if pd.isnull(data_ref):
            continue

        # --- MUDANÇA AQUI: Cálculo em ANOS ---
        # Dias / 365.25
        idade_anos = (agora - data_ref).days / 365.25

        if idade_anos < 0:
            idade_anos = 0

        qtd_falhas = dict_falhas.get(tag, 0)

        if qtd_falhas == 0:
            mtbf = idade_anos
        else:
            mtbf = idade_anos / qtd_falhas

        mtbf_values.append(mtbf)

    if not mtbf_values:
        return 0

    media_mtbf = sum(mtbf_values) / len(mtbf_values)

    # Retorna com 1 casa decimal (ex: 2.5 anos)
    return round(media_mtbf, 1)


def get_mttr_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o MTTR (Mean Time To Repair) em DIAS.
    Fórmula: SUM(Fechamento - Abertura) / COUNT(OS Únicas)
    Filtros:
      - Date Range: fechamento
      - Tipo: CORRETIVA
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Garante Data de Fechamento e Abertura
    if 'fechamento' not in df.columns or 'abertura' not in df.columns:
        return 0

    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    df = df.dropna(subset=['fechamento', 'abertura'])

    # 2. Filtro de Data (Ref: FECHAMENTO)
    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]

    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Tipo: Corretiva
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    if df.empty:
        return 0

    # 4. MenosDuplicadas (OS + Tag + Local)
    # Garante que cada OS conta apenas uma vez para o denominador e numerador
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Cálculo do Tempo (Dias)
    # Total Seconds / 86400 = Dias com fração (ex: 1.5 dias)
    df['tempo_dias'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400

    # Remove inconsistências (negativos)
    df = df[df['tempo_dias'] >= 0]

    if df.empty:
        return 0

    # 6. Aplicação da Fórmula
    soma_tempo = df['tempo_dias'].sum()
    count_os = df.shape[0]  # COUNT_DISTINCT já feito pelo drop_duplicates

    if count_os == 0:
        return 0

    mttr = soma_tempo / count_os

    return round(mttr, 2)  # Retorna com 2 casas decimais


def get_tempo_medio_primeiro_atendimento_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o Tempo Médio para Primeiro Atendimento (em Horas).
    Fórmula: AVG(Data Atendimento - Abertura)
    Filtros:
      - Date Range: abertura
      - Situação: Fechada
      - Ocorrência: Exclui 'ATIVIDADE PROGRAMADA'
      - SemChamado: Exclui data_chamado Nula (ou data_atendimento se for o caso)
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Garante Datas (Abertura e Atendimento)
    # Se 'data_chamado' for crucial para o filtro, verifique se ela existe.
    # Assumindo que o cálculo é Atendimento - Abertura conforme sua descrição.
    cols_datas = ['abertura', 'data_atendimento']
    for col in cols_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    df = df.dropna(subset=['abertura', 'data_atendimento'])

    # 2. Filtro de Data (Ref: ABERTURA)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]

    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Situação: Fechada
    if 'situacao' in df.columns:
        df = df[df['situacao'].str.lower() == 'fechada']

    # 4. Filtro Ocorrência: Excluir 'ATIVIDADE PROGRAMADA'
    if 'ocorrencia' in df.columns:
        df = df[df['ocorrencia'].str.upper() != 'ATIVIDADE PROGRAMADA']

    # 5. Filtro SemChamado (Excluir Data Chamado Nula)
    # Se a coluna existir, aplica o filtro.
    if 'data_chamado' in df.columns:
        df = df[df['data_chamado'].notnull()]

    if df.empty:
        return 0

    # 6. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 7. Cálculo (Horas)
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    # Remove inconsistências (Atendimento antes da abertura)
    df = df[df['tempo_horas'] >= 0]

    if df.empty:
        return 0

    media_horas = df['tempo_horas'].mean()

    return round(media_horas, 2)


def get_tempo_mediano_primeiro_atendimento_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a MEDIANA do Tempo para Primeiro Atendimento (em Horas).
    Fórmula: MEDIAN(Data Atendimento - Abertura)
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Garante Datas
    cols_datas = ['abertura', 'data_atendimento']
    for col in cols_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    df = df.dropna(subset=['abertura', 'data_atendimento'])

    # 2. Filtro de Data (Ref: ABERTURA)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtros de Negócio (Mesmos do TMA Médio)
    if 'situacao' in df.columns:
        df = df[df['situacao'].str.lower() == 'fechada']

    if 'ocorrencia' in df.columns:
        df = df[df['ocorrencia'].str.upper() != 'ATIVIDADE PROGRAMADA']

    if 'data_chamado' in df.columns:
        df = df[df['data_chamado'].notnull()]

    if df.empty:
        return 0

    # 4. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Cálculo (Horas)
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['tempo_horas'] >= 0]

    if df.empty:
        return 0

    # --- DIFERENÇA AQUI: MEDIAN ---
    mediana_horas = df['tempo_horas'].median()

    return round(mediana_horas, 2)
