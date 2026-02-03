import pandas as pd
import numpy as np
from django.db.models import Count
from ...models import ConsultaOs


def get_total_equipamentos_cadastrados(df_equip, data_inicio=None, data_fim=None):
    """
    Retorna a quantidade de equipamentos cuja data de CADASTRO está no período.
    Usado na tela de Indicadores.
    """
    if df_equip.empty:
        return 0

    df = df_equip.copy()

    # 1. Copia e Deduplica (Tag única)
    # Não precisamos agrupar por empresa, pois queremos o totalzão (ou o total da empresa filtrada)

    if 'cadastro' in df.columns:
        df['cadastro'] = pd.to_datetime(df['cadastro'], errors='coerce')

        if data_inicio:
            df = df[df['cadastro'] >= pd.to_datetime(data_inicio)]

        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['cadastro'] <= fim]

    if df.empty:
        return 0

    if 'tag' in df.columns:
        # Remove Nulos (None/NaN)
        df = df.dropna(subset=['tag'])

        # Remove Vazios (String vazia '')
        df = df[df['tag'] != '']

        # Remove Duplicatas
        df = df.drop_duplicates(subset=['tag'])

    # 2. Retorna a contagem total de linhas
    return df.shape[0]


def get_total_os_corretivas(df_os, data_inicio=None, data_fim=None):
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

    # 1. Garante conversão de data (fechamento)
    if 'fechamento' in df.columns:
        df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
        df = df.dropna(subset=['fechamento'])
    else:
        return 0

    # 2. Filtro de Data (Dimension: Fechamento)
    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]

    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

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


def get_tempo_medio_primeiro_atendimento_critico_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o TMA (Tempo Médio Atendimento) apenas para chamados CRÍTICOS.
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - Prioridade: ALTA
      - MenosDuplicadas
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

    # 3. Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 4. Filtro Prioridade: ALTA (CRÍTICA)
    # Usamos str.contains para pegar 'ALTA', 'URGENTE', etc, se houver variações,
    # ou comparação direta se for padronizado.
    if 'prioridade' in df.columns:
        df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 6. Cálculo (Horas)
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['tempo_horas'] >= 0]

    if df.empty:
        return 0

    media_horas = df['tempo_horas'].mean()

    return round(media_horas, 2)


def get_tempo_mediano_primeiro_atendimento_critico_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a MEDIANA do Tempo para Primeiro Atendimento Critico (em Horas).
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

    # 3. Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 4. Filtro Prioridade: ALTA (CRÍTICA)
    # Usamos str.contains para pegar 'ALTA', 'URGENTE', etc, se houver variações,
    # ou comparação direta se for padronizado.
    if 'prioridade' in df.columns:
        df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 6. Cálculo (Horas)
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['tempo_horas'] >= 0]

    if df.empty:
        return 0

    mediana_horas = df['tempo_horas'].median()

    return round(mediana_horas, 2)


def get_tempo_medio_equipamento_critico_parado_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a Média de Tempo Parado (Downtime) para Equipamentos Críticos (Horas).
    Fórmula: AVG(Funcionamento - Parada)
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - Prioridade: ALTA
      - Exclude: Parada/Funcionamento isNull
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Garante Datas
    cols_datas = ['abertura', 'parada', 'funcionamento']
    for col in cols_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Garante que temos as datas de cálculo do downtime
    df = df.dropna(subset=['parada', 'funcionamento'])

    # 2. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        # Remove linhas sem abertura para garantir filtro correto
        df = df.dropna(subset=['abertura'])

        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]
    else:
        return 0

    if df.empty:
        return 0

    # 3. Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 4. Filtro Prioridade: ALTA (CRÍTICA)
    if 'prioridade' in df.columns:
        df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 6. Cálculo (Horas)
    df['tempo_parada_horas'] = (df['funcionamento'] - df['parada']).dt.total_seconds() / 3600

    # Remove inconsistências (Funcionamento antes da Parada)
    df = df[df['tempo_parada_horas'] >= 0]

    if df.empty:
        return 0

    media_horas = df['tempo_parada_horas'].mean()

    return round(media_horas, 2)


def get_tempo_mediano_equipamento_critico_parado_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a Média de Tempo Parado (Downtime) para Equipamentos Críticos (Horas).
    Fórmula: AVG(Funcionamento - Parada)
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - Prioridade: ALTA
      - Exclude: Parada/Funcionamento isNull
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Garante Datas
    cols_datas = ['abertura', 'parada', 'funcionamento']
    for col in cols_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Garante que temos as datas de cálculo do downtime
    df = df.dropna(subset=['parada', 'funcionamento'])

    # 2. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        # Remove linhas sem abertura para garantir filtro correto
        df = df.dropna(subset=['abertura'])

        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]
    else:
        return 0

    if df.empty:
        return 0

    # 3. Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 4. Filtro Prioridade: ALTA (CRÍTICA)
    if 'prioridade' in df.columns:
        df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 6. Cálculo (Horas)
    df['tempo_parada_horas'] = (df['funcionamento'] - df['parada']).dt.total_seconds() / 3600

    # Remove inconsistências (Funcionamento antes da Parada)
    df = df[df['tempo_parada_horas'] >= 0]

    if df.empty:
        return 0

    media_horas = df['tempo_parada_horas'].median()

    return round(media_horas, 2)


def get_taxa_disponibilidade_kpi(df_os, df_equip, data_inicio=None, data_fim=None):
    """
    Calcula a Taxa de Disponibilidade (%).
    Fórmula: (Horas Totais Potenciais - Horas Parado) / Horas Totais Potenciais
    Onde:
      - Horas Totais = 24 * Dias no Período * Qtd Equipamentos (Inventário)
      - Horas Parado = Soma(Fechamento - Abertura) das Corretivas
    """
    # 1. Definição do Período (Dias)
    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        dias_periodo = (dt_fim - dt_ini).days + 1
    else:
        # Se não tiver filtro, tenta estimar pelos dados ou usa padrão 30 dias
        dias_periodo = 30
        if not df_os.empty and 'abertura' in df_os.columns:
            # Fallback: Max - Min dos dados
            dias_periodo = (df_os['abertura'].max() - df_os['abertura'].min()).days + 1

    if dias_periodo < 1:
        dias_periodo = 1

    # 2. Qtd Equipamentos (Denominador) - Baseado no Inventário Filtrado
    # Se df_equip estiver vazio, retornamos 0 para evitar divisão por zero
    if df_equip.empty:
        qtd_equipamentos = 0
    else:
        # Conta tags únicas do cadastro
        # (Supõe que df_equip já veio filtrado pela View se necessário, ou representa o parque todo)
        # Importante: Limpar vazios
        df_e = df_equip.copy()
        if 'tag' in df_e.columns:
            df_e = df_e.dropna(subset=['tag'])
            df_e = df_e[df_e['tag'] != '']
            qtd_equipamentos = df_e['tag'].nunique()
        else:
            qtd_equipamentos = 0

    if qtd_equipamentos == 0:
        return 0

    # 3. Horas Parado (Numerador) - Baseado nas OS Corretivas
    horas_parado = 0
    if not df_os.empty:
        df = df_os.copy()

        # Filtros e Limpeza (Igual ao MTTR)
        cols = ['abertura', 'fechamento']  # Ou data_solucao
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors='coerce')

        df = df.dropna(subset=cols)

        # Filtro Data
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

        # Filtro Tipo (Corretiva)
        if 'tipomanutencao' in df.columns:
            df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

        # Filtro Duplicatas
        df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

        # Soma do Tempo (em Horas)
        # TempoParaResolver = fechamento - abertura
        df['downtime'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 3600
        df = df[df['downtime'] > 0]

        horas_parado = df['downtime'].sum()

    # 4. Cálculo Final
    # Horas Potenciais = 24h * Dias * Qtd Maquinas
    horas_totais_potenciais = 24 * dias_periodo * qtd_equipamentos

    if horas_totais_potenciais == 0:
        return 0

    taxa = (horas_totais_potenciais - horas_parado) / horas_totais_potenciais

    # Retorna em Porcentagem (ex: 98.5)
    return round(taxa * 100, 2)
