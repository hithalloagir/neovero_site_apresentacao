import pandas as pd
import numpy as np
from django.db.models import Count


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


def get_mtbf_medio_kpi(df_equip, df_os):
    """
    Calcula o MTBF Médio em ANOS usando apenas Pandas.
    Fórmula: Idade do Equipamento / Quantidade de Falhas (Corretivas)
    """
    if df_equip.empty:
        return 0

    # 1. Obter lista de tags do DF de equipamentos
    tags = df_equip['tag'].dropna().unique().tolist()
    if not tags:
        return 0

    # 2. Contar falhas usando df_os (SUBSTITUI A QUERY AO BANCO)
    dict_falhas = {}
    if not df_os.empty:
        # Filtra Corretivas e Tags relevantes
        df_falhas = df_os[
            (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
            (df_os['tag'].isin(tags))
        ]
        # Conta ocorrências por tag
        if not df_falhas.empty:
            dict_falhas = df_falhas['tag'].value_counts().to_dict()

    mtbf_values = []
    agora = pd.Timestamp.now()

    for _, row in df_equip.iterrows():
        tag = row['tag']
        data_ref = row['instalacao'] if pd.notnull(row['instalacao']) else row['cadastro']

        if pd.isnull(data_ref):
            continue

        # Cálculo da Idade em Anos
        idade_anos = (agora - data_ref).days / 365.25

        if idade_anos < 0:
            idade_anos = 0

        # Pega qtd de falhas do dicionário calculado via Pandas
        qtd_falhas = dict_falhas.get(tag, 0)

        if qtd_falhas == 0:
            mtbf = idade_anos
        else:
            mtbf = idade_anos / qtd_falhas

        mtbf_values.append(mtbf)

    if not mtbf_values:
        return 0

    media_mtbf = sum(mtbf_values) / len(mtbf_values)

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


def get_taxa_disponibilidade_criticos_kpi(df_os, df_equip, data_inicio=None, data_fim=None):
    """
    Calcula a Taxa de Disponibilidade (%) APENAS para Equipamentos Críticos.
    Definição de Crítico: Equipamento que possui OS com prioridade 'ALTA' no conjunto de dados.
    """
    # 1. Definição do Período (Dias)
    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        dias_periodo = (dt_fim - dt_ini).days + 1
    else:
        dias_periodo = 30
        if not df_os.empty and 'abertura' in df_os.columns:
            dias_periodo = (df_os['abertura'].max() - df_os['abertura'].min()).days + 1

    if dias_periodo < 1:
        dias_periodo = 1

    # 2. Identificar o Universo de Equipamentos Críticos (O "Agregado")
    # Precisamos saber QUANTOS equipamentos são críticos para calcular as horas potenciais totais.
    if df_os.empty or df_equip.empty:
        return 0

    # Acha tags que tiveram prioridade ALTA (no período carregado)
    # Se você quiser ser mais preciso, precisaria do histórico total, mas usaremos o recorte atual.
    tags_criticas = []
    if 'prioridade' in df_os.columns and 'tag' in df_os.columns:
        tags_criticas = df_os[
            df_os['prioridade'].str.upper().str.contains('ALTA', na=False)
        ]['tag'].unique()

    if len(tags_criticas) == 0:
        return 0  # Se não tem equipamento crítico, não tem indicador

    # Cruza com df_equip para garantir que são equipamentos ativos/cadastrados
    df_e_crit = df_equip[df_equip['tag'].isin(tags_criticas)].copy()

    # Limpeza de duplicatas/vazios
    if 'tag' in df_e_crit.columns:
        df_e_crit = df_e_crit.dropna(subset=['tag'])
        df_e_crit = df_e_crit[df_e_crit['tag'] != '']
        qtd_equipamentos_criticos = df_e_crit['tag'].nunique()
    else:
        qtd_equipamentos_criticos = 0

    if qtd_equipamentos_criticos == 0:
        return 0

    # 3. Calcular Horas Parado (Downtime) DOS CRÍTICOS
    horas_parado = 0

    # Filtra OS para cálculo (Datas + Tipo + Prioridade + Duplicatas)
    df = df_os.copy()

    # Conversão de datas
    for c in ['abertura', 'fechamento']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce')
    df = df.dropna(subset=['abertura', 'fechamento'])

    # Filtro Data
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    # Filtro: Apenas as tags que identificamos como críticas
    df = df[df['tag'].isin(tags_criticas)]

    # Filtro Tipo (Corretiva) - Disponibilidade geralmente olha para quebras
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # Filtro Duplicatas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Cálculo Downtime
    df['downtime'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['downtime'] > 0]

    horas_parado = df['downtime'].sum()

    # 4. Cálculo Final
    # Horas Potenciais = 24h * Dias * Qtd Equipamentos Críticos
    horas_totais_potenciais = 24 * dias_periodo * qtd_equipamentos_criticos

    if horas_totais_potenciais == 0:
        return 0

    taxa = (horas_totais_potenciais - horas_parado) / horas_totais_potenciais

    return round(taxa * 100, 2)


def get_qtde_equipamentos_indisponiveis_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Retorna a quantidade de equipamentos que ficaram INDISPONÍVEIS no período.
    Lógica: Equipamentos com OS onde o campo 'parada' está preenchido.
    Filtros:
      - Date Range: abertura
      - Indisponível: Parada IS NOT NULL
      - MenosDuplicadas (Conta equipamentos únicos afetados)
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    if 'parada' in df.columns:
        df['parada'] = pd.to_datetime(df['parada'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA)
    # Queremos saber: Quantos equipamentos quebraram (abriram OS com parada) neste período?
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. FILTRO "INDISPONÍVEIS" (Onde parada existe)
    # Se tem data de parada, gerou indisponibilidade.
    df = df.dropna(subset=['parada'])

    if df.empty:
        return 0

    # 4. Contagem Distinta de Equipamentos (Tags)
    # Se o mesmo equipamento parou 3 vezes no mês, conta como 1 equipamento "problemático" no KPI?
    # Geralmente KPIs de "Quantidade de Equipamentos" contam itens únicos.
    df = df.drop_duplicates(subset=['tag'])

    return df.shape[0]


def get_qtde_equipamentos_criticos_indisponiveis_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Retorna a quantidade de equipamentos CRÍTICOS que ficaram INDISPONÍVEIS.
    Filtros:
      - Date Range: abertura
      - Indisponível: Parada IS NOT NULL
      - Crítico: Prioridade contém 'ALTA'
      - MenosDuplicadas (Conta equipamentos únicos afetados)
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    if 'parada' in df.columns:
        df['parada'] = pd.to_datetime(df['parada'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. FILTRO INDISPONÍVEIS (Tem data de parada)
    df = df.dropna(subset=['parada'])

    # 4. FILTRO CRÍTICOS (Prioridade ALTA)
    if 'prioridade' in df.columns:
        df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]

    if df.empty:
        return 0

    # 5. Contagem Distinta de Tags
    df = df.drop_duplicates(subset=['tag'])

    return df.shape[0]


def get_taxa_resolucao_corretivas_periodo_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a % de OS Corretivas que foram Abertas E Fechadas dentro do mesmo período selecionado.
    Fórmula: (OS Abertas e Fechadas no Periodo) / (Total OS Abertas no Periodo)
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas
    for col in ['abertura', 'fechamento']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA) - Define o Denominador
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            # Garante o final do dia
            fim_periodo = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim_periodo]
    else:
        return 0

    if df.empty:
        return 0

    # 3. Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']

    # 4. MenosDuplicadas (Universo de OS únicas abertas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    total_abertas = df.shape[0]

    if total_abertas == 0:
        return 0

    # 5. Numerador: Quantas dessas também fecharam dentro do prazo limite?
    # A data de fechamento deve existir (não nula) e ser <= data_fim do filtro
    # (Não precisa ser >= data_inicio pois logicamente não tem como fechar antes de abrir,
    # e a abertura já é >= data_inicio)

    if data_fim:
        fim_periodo = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        resolvidas = df[
            (df['fechamento'].notnull()) &
            (df['fechamento'] <= fim_periodo)
        ]
    else:
        # Se não tem data fim definida, considera todas as fechadas
        resolvidas = df[df['fechamento'].notnull()]

    total_resolvidas = resolvidas.shape[0]

    # 6. Cálculo %
    taxa = (total_resolvidas / total_abertas) * 100

    return round(taxa, 2)


def get_pendencias_corretiva_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula a média de pendências por equipamento afetado.
    Fórmula: (Soma(Abertas) + Soma(Pendentes)) / CountDistinct(Tag)
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - Situação: ABERTA ou PENDENTE
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
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

    # 4. Filtro Situação (Numerador foca apenas nessas)
    if 'situacao' in df.columns:
        # Normaliza para garantir
        status_pendentes = ['ABERTA', 'PENDENTE']
        df = df[df['situacao'].str.upper().isin(status_pendentes)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas (OS Únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 6. Cálculo
    # Numerador: Quantidade total de OSs que sobraram (que são abertas ou pendentes)
    total_pendencias = df.shape[0]

    # Denominador: Quantos equipamentos distintos estão nessa situação?
    total_equipamentos_afetados = df['tag'].nunique()

    if total_equipamentos_afetados == 0:
        return 0

    media_pendencias = total_pendencias / total_equipamentos_afetados

    return round(media_pendencias, 2)


def get_cumprimento_preventiva_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o % de Cumprimento de Preventivas.
    Fórmula: (Preventivas Fechadas / Total Preventivas Abertas) * 100
    Filtros:
      - Date Range: abertura
      - Tipo: PREVENTIVA
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas (se ainda não foi feito)
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA - Define o Universo Planejado/Aberto no Mês)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Tipo: PREVENTIVA
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'PREVENTIVA']

    # 4. MenosDuplicadas (OS Únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Denominador: Total de Preventivas Abertas no período
    total_preventivas = df.shape[0]

    if total_preventivas == 0:
        return 0

    # 5. Numerador: Quantas dessas estão FECHADAS?
    # Não importa se fechou hoje ou mês que vem (se a regra for apenas status "Fechada"),
    # mas geralmente "Cumprimento" olha o status atual.
    if 'situacao' in df.columns:
        fechadas = df[df['situacao'].str.lower() == 'fechada']
        total_fechadas = fechadas.shape[0]
    else:
        total_fechadas = 0

    # 6. Cálculo %
    taxa = (total_fechadas / total_preventivas) * 100

    return round(taxa, 2)


def get_cumprimento_calibracao_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o % de Cumprimento de Calibração.
    Fórmula: (Preventivas Fechadas / Total Calibração Abertas) * 100
    Filtros:
      - Date Range: abertura
      - Tipo: CALIBRAÇÃO
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas (se ainda não foi feito)
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA - Define o Universo Planejado/Aberto no Mês)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Tipo: CALIBRAÇÃO
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'CALIBRAÇÃO']

    # 4. MenosDuplicadas (OS Únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Denominador: Total de Calibração Abertas no período
    total_calibracao = df.shape[0]

    if total_calibracao == 0:
        return 0

    # 5. Numerador: Quantas dessas estão FECHADAS?
    # Não importa se fechou hoje ou mês que vem (se a regra for apenas status "Fechada"),
    # mas geralmente "Cumprimento" olha o status atual.
    if 'situacao' in df.columns:
        fechadas = df[df['situacao'].str.lower() == 'fechada']
        total_fechadas = fechadas.shape[0]
    else:
        total_fechadas = 0

    # 6. Cálculo %
    taxa = (total_fechadas / total_calibracao) * 100

    return round(taxa, 2)


def get_cumprimento_treinamento_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o % de Cumprimento de Treinamento.
    Fórmula: (Preventivas Fechadas / Total Treinamento Abertas) * 100
    Filtros:
      - Date Range: abertura
      - Tipo: 'TREINAMENTO'
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas (se ainda não foi feito)
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA - Define o Universo Planejado/Aberto no Mês)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Tipo: TREINAMENTO
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'TREINAMENTO']

    # 4. MenosDuplicadas (OS Únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Denominador: Total de Treinamento Abertas no período
    total_treinamento = df.shape[0]

    if total_treinamento == 0:
        return 0

    # 5. Numerador: Quantas dessas estão FECHADAS?
    # Não importa se fechou hoje ou mês que vem (se a regra for apenas status "Fechada"),
    # mas geralmente "Cumprimento" olha o status atual.
    if 'situacao' in df.columns:
        fechadas = df[df['situacao'].str.lower() == 'fechada']
        total_fechadas = fechadas.shape[0]
    else:
        total_fechadas = 0

    # 6. Cálculo %
    taxa = (total_fechadas / total_treinamento) * 100

    return round(taxa, 2)


def get_cumprimento_tse_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Calcula o % de Cumprimento de TSE.
    Fórmula: (Preventivas Fechadas / Total TSE Abertas) * 100
    Filtros:
      - Date Range: abertura
      - Tipo: 'TREINAMENTO'
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas (se ainda não foi feito)
    if 'abertura' in df.columns:
        df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA - Define o Universo Planejado/Aberto no Mês)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
        if data_inicio:
            df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
        if data_fim:
            fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
            df = df[df['abertura'] <= fim]

    if df.empty:
        return 0

    # 3. Filtro Tipo: TSE
    if 'tipomanutencao' in df.columns:
        df = df[df['tipomanutencao'].str.upper() == 'TESTE DE SEGURANÇA ELÉTRICA - TSE']

    # 4. MenosDuplicadas (OS Únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Denominador: Total de TSE Abertas no período
    total_tse = df.shape[0]

    if total_tse == 0:
        return 0

    # 5. Numerador: Quantas dessas estão FECHADAS?
    # Não importa se fechou hoje ou mês que vem (se a regra for apenas status "Fechada"),
    # mas geralmente "Cumprimento" olha o status atual.
    if 'situacao' in df.columns:
        fechadas = df[df['situacao'].str.lower() == 'fechada']
        total_fechadas = fechadas.shape[0]
    else:
        total_fechadas = 0

    # 6. Cálculo %
    taxa = (total_fechadas / total_tse) * 100

    return round(taxa, 2)


def get_qtde_reparos_imediato_kpi(df_os, data_inicio=None, data_fim=None):
    """
    Retorna a quantidade de Reparos realizados em menos de 1 minuto (Imediatos).
    Filtros:
      - Date Range: abertura
      - Tipo: CORRETIVA
      - TempoReparo: (Fechamento - Abertura) < 60 segundos
      - MenosDuplicadas
    """
    if df_os.empty:
        return 0

    df = df_os.copy()

    # 1. Conversão de Datas
    for col in ['abertura', 'fechamento']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 2. Filtro de Data (Ref: ABERTURA)
    if 'abertura' in df.columns:
        df = df.dropna(subset=['abertura'])
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

    # 4. Filtro Tempo de Reparo OK (IMEDIATO < 1 min)
    # Garante que tem fechamento
    df = df.dropna(subset=['fechamento'])

    # Calcula duração em segundos
    df['duracao_segundos'] = (df['fechamento'] - df['abertura']).dt.total_seconds()

    # Aplica a regra: Menor que 60 segundos (e não negativo)
    df = df[(df['duracao_segundos'] < 60) & (df['duracao_segundos'] >= 0)]

    if df.empty:
        return 0

    # 5. MenosDuplicadas (Conta OSs únicas)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    return df.shape[0]


def get_os_corretivas_ultimos_3_anos_por_familia(df_os, df_equip):
    """
    Retorna uma lista de dicionários com o total de Corretivas por Família (Top 20).
    Considera apenas OSs abertas nos últimos 3 anos (36 meses) para os equipamentos filtrados.
    """
    if df_os.empty or df_equip.empty:
        return []

    # 1. Preparar Equipamentos (Já vêm filtrados por Cadastro da View)
    # Precisamos apenas de Tag e Família
    df_e = df_equip.copy()
    if 'tag' not in df_e.columns or 'familia' not in df_e.columns:
        return []

    # Limpeza básica
    df_e = df_e.dropna(subset=['tag', 'familia'])
    df_e = df_e[df_e['familia'] != '']
    # Garante tags únicas no cadastro (se houver duplicidade, pega a primeira)
    df_e = df_e.drop_duplicates(subset=['tag'])

    # 2. Preparar OS (Filtro "Últimos 3 Anos")
    df_o = df_os.copy()

    # Conversão de data
    if 'abertura' in df_o.columns:
        df_o['abertura'] = pd.to_datetime(df_o['abertura'], errors='coerce')
    else:
        return []

    # Filtro Temporal: Últimos 3 Anos (baseado em HOJE)
    hoje = pd.Timestamp.now()
    tres_anos_atras = hoje - pd.DateOffset(years=3)

    df_o = df_o[df_o['abertura'] >= tres_anos_atras]

    if df_o.empty:
        return []

    # Filtro Tipo: CORRETIVA
    if 'tipomanutencao' in df_o.columns:
        df_o = df_o[df_o['tipomanutencao'].str.upper() == 'CORRETIVA']

    # Filtro MenosDuplicadas
    df_o = df_o.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 3. Cruzamento (Merge)
    # Inner Join: Só queremos OSs de equipamentos que estão no filtro de cadastro atual
    df_merged = pd.merge(df_o, df_e[['tag', 'familia']], on='tag', how='inner')

    if df_merged.empty:
        return []

    # 4. Agrupamento por Família
    # Conta quantidade de OSs (usando a coluna 'os' ou qualquer outra não nula)
    agrupado = df_merged.groupby('familia')['os'].count().reset_index()
    agrupado.columns = ['familia', 'qtd_corretivas']

    # Ordenar Decrescente
    agrupado = agrupado.sort_values(by='qtd_corretivas', ascending=False)

    # Retorna Top N (ex: 20) ou tudo, formato lista de dicts para o template
    return agrupado.head(20).to_dict('records')
