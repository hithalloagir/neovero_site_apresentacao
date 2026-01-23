
import pandas as pd
import os
from django.conf import settings
from ...models import ConsultaOs


def get_tempo_medio_atendimento_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula métricas filtradas por data e empresa.
    """
    # 1. Pré-filtro no Banco de Dados (Melhora performance)
    # Só trazemos do banco o que for da empresa selecionada
    queryset = ConsultaOs.objects.all().values('abertura', 'data_atendimento', 'empresa')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    # 2. Criação do DataFrame
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 3. Conversão de Datas (ETL)
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df['data_atendimento'] = pd.to_datetime(df['data_atendimento'], errors='coerce')

    # Remove datas inválidas
    df = df.dropna(subset=['abertura', 'data_atendimento'])

    # 4. Filtro de DATA (No Pandas)
    # Como convertemos para datetime acima, agora podemos comparar matematicamente
    if data_inicio:
        # Garante que data_inicio seja datetime para comparação
        data_inicio = pd.to_datetime(data_inicio)
        df = df[df['abertura'] >= data_inicio]

    if data_fim:
        data_fim = pd.to_datetime(data_fim)
        # Ajuste para pegar o final do dia (23:59:59) se necessário, ou usar dia seguinte
        data_fim = data_fim.replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= data_fim]

    # Se após o filtro o dataframe ficar vazio
    if df.empty:
        return [], []

    # 5. Cálculos (Lógica de Negócio)
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['tempo_horas'] >= 0]  # Remove inconsistências

    # 6. Agrupamento por Unidade
    df_agrupado = df.groupby('empresa')['tempo_horas'].mean().reset_index()
    df_agrupado['tempo_horas'] = df_agrupado['tempo_horas'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_horas', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_horas'].tolist()


def get_dispersao_reparo_atendimento(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna dados para o gráfico de dispersão (Scatter Plot):
    Eixo X: Tempo de Reparo (Dias)
    Eixo Y: Tempo de Atendimento (Horas)
    """

    # 1. Busca apenas os dados necessários para o cálculo e identificação
    queryset = ConsultaOs.objects.filter(situacao__iexact='Fechada').values(
        'abertura', 'fechamento', 'data_atendimento', 'empresa', 'equipamento'
    )

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    # 2. Carrega para o Pandas
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return []

    # 3. Conversão e Limpeza de Datas
    cols_data = ['abertura', 'fechamento', 'data_atendimento']

    for col in cols_data:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Remove linhas onde qualquer data essencial seja inválida (NaT)
    df.dropna(subset=cols_data, inplace=True)

    # 4. Filtro de Período (Intervalo de Datas)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]

    if data_fim:
        # Garante o dia inteiro (até 23:59:59)
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return []

    # 5. Cálculos das Métricas
    # Eixo X: Dias | Eixo Y: Horas
    df['x'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400  # 86400s = 1 dia
    df['y'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    # 6. Remove inconsistências (Tempos negativos)
    df = df[(df['x'] >= 0) & (df['y'] >= 0)]

    # 7. Formatação Final
    df = df.sort_values(by='x', ascending=True)
    df = df.rename(columns={'equipamento': 'familia'})

    # Retorna lista de dicionários otimizada
    return df[['x', 'y', 'empresa', 'familia']].to_dict(orient='records')


def get_tempo_medio_reparo_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula o tempo médio de reparo por unidade (empresa).
    """

    # 1. Pré-filtro no Banco de Dados
    queryset = ConsultaOs.objects.filter(situacao__iexact='Fechada').values(
        'abertura', 'fechamento', 'empresa', 'situacao',
    )

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    # 2. Criação do DataFrame
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 3. Conversão de Datas
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')

    # Remove datas inválidas
    df = df.dropna(subset=['abertura', 'fechamento'])

    # 4. Filtro de DATA
    if data_inicio:
        data_inicio = pd.to_datetime(data_inicio)
        df = df[df['abertura'] >= data_inicio]

    if data_fim:
        data_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= data_fim]

    if df.empty:
        return [], []

    # 5. Cálculos
    df['tempo_dias'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400
    df = df[df['tempo_dias'] >= 0]  # Remove inconsistências

    # 6. Agrupamento por Unidade
    df_agrupado = df.groupby('empresa')['tempo_dias'].mean().reset_index()
    df_agrupado['tempo_dias'] = df_agrupado['tempo_dias'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_dias', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_dias'].tolist()


def get_taxa_cumprimento_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula a Taxa de Cumprimento (%) para PREV, CALIB, QUALI e TSE.
    Fórmula: (Qtd Fechada / Total de OS) * 100
    """
    tipos_alvo = ["PREVENTIVA", "CALIBRAÇÃO", "QUALIFICAÇÃO", "TSE"]

    queryset = ConsultaOs.objects.filter(tipomanutencao__in=tipos_alvo).values(
        'abertura', 'situacao', 'empresa', 'tipomanutencao'
    )

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df['is_fechada'] = df['situacao'].astype(str).str.lower() == 'fechada'
    df['is_fechada'] = df['is_fechada'].astype(int)

    df_agrupado = df.groupby('empresa')['is_fechada'].agg(['sum', 'count']).reset_index()

    # Fórmula: (Soma Fechadas / Total Geral) * 100
    df_agrupado['taxa'] = (df_agrupado['sum'] / df_agrupado['count']) * 100

    # Arredonda para 2 casas
    df_agrupado['taxa'] = df_agrupado['taxa'].round(2)

    # Ordena: Quem tem maior cumprimento primeiro
    df_agrupado = df_agrupado.sort_values(by='taxa', ascending=False)

    return (
        df_agrupado['empresa'].tolist(),
        df_agrupado['taxa'].tolist(),
        df_agrupado['sum'].astype(int).tolist(),   # Qtd Fechada (converte float pra int)
        df_agrupado['count'].astype(int).tolist()  # Total OS
    )


def get_qtde_os_por_tipo_manutencao(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna a quantidade de OS por Tipo de Manutenção.
    Regra de Unicidade: Remove linhas se (os + tag + local_api) forem idênticos.
    """
    queryset = ConsultaOs.objects.all().values(
        'os', 'tag', 'local_api', 'tipomanutencao', 'empresa', 'abertura'
    )

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['tipomanutencao'].value_counts()

    labels = contagem.index.tolist()
    data = contagem.values.tolist()

    return labels, data


def get_qtde_os_planejadas_realizadas(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna a quantidade de OS Planejadas (Causa=Planejamento) que foram Fechadas.
    Data de referência: Fechamento.
    """
    queryset = ConsultaOs.objects.filter(
        causa__iexact='PLANEJAMENTO',
        situacao__iexact='Fechada'
    ).values('os', 'empresa', 'fechamento', 'tag', 'local_api')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 3. Tratamento de Data (Referência: FECHAMENTO)
    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
    df.dropna(subset=['fechamento'], inplace=True)

    # Filtro de Data
    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        # Garante o dia inteiro
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['empresa'].value_counts()

    labels = contagem.index.tolist()
    data = contagem.values.tolist()

    return labels, data


def get_qtde_os_planejadas_n_realizadas(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna a quantidade de OS Planejadas (Causa=Planejamento) que NÃO foram Fechadas.
    Geralmente excluímos 'Cancelada' para pegar só o passivo real.
    Data de referência: ABERTURA (pois não tem fechamento).
    """
    queryset = ConsultaOs.objects.filter(
        causa__iexact='PLANEJAMENTO',
    ).exclude(
        situacao__in=['Fechada', 'Cancelada']
    ).values('os', 'empresa', 'abertura', 'tag', 'local_api')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['empresa'].value_counts()

    labels = contagem.index.tolist()
    data = contagem.values.tolist()

    return labels, data


def get_os_taxa_conclusao_planejamento(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula a % de Conclusão de OS de Planejamento.
    Fórmula: (Planejadas Fechadas / Total Planejadas Válidas) * 100
    *Total Válidas = Fechadas + Pendentes (Exclui Canceladas)
    """

    # 1. Busca TODO o universo de Planejamento (Exceto Canceladas)
    queryset = ConsultaOs.objects.filter(
        causa__iexact='Planejamento'
    ).exclude(
        situacao__iexact='Cancelada'  # Removemos canceladas do cálculo de meta
    ).values('os', 'empresa', 'situacao', 'tag', 'local_api', 'fechamento', 'abertura')

    # 2. Filtro de Empresa
    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], [], [], []

    # 3. Tratamento de Data
    # DICA: Para cálculo de taxa, geralmente usamos a 'abertura' ou 'fechamento' como base.
    # Se você quer ver a taxa do planejamento DE JANEIRO, use a data de competência (abertura ou uma data_programada).
    # Aqui usaremos 'abertura' para ser consistente com o gráfico de Pendências.
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], [], [], []

    # 4. REMOÇÃO DE DUPLICATAS
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Cálculo das Métricas
    # Cria coluna binária: 1 se Fechada, 0 se não (Aberta, Pendente, etc)
    df['is_fechada'] = df['situacao'].astype(str).str.lower() == 'fechada'
    df['is_fechada'] = df['is_fechada'].astype(int)

    # Agrupa
    df_agrupado = df.groupby('empresa')['is_fechada'].agg(['sum', 'count']).reset_index()
    # sum = Quantidade Fechada
    # count = Total Planejado (Universo)

    # Calcula %
    df_agrupado['taxa'] = (df_agrupado['sum'] / df_agrupado['count']) * 100
    df_agrupado['taxa'] = df_agrupado['taxa'].round(2)

    # Ordena melhor desempenho primeiro
    df_agrupado = df_agrupado.sort_values(by='taxa', ascending=False)

    # Retorna: Labels, Taxas, Numerador, Denominador (para o Tooltip)
    return (
        df_agrupado['empresa'].tolist(),
        df_agrupado['taxa'].tolist(),
        df_agrupado['sum'].astype(int).tolist(),
        df_agrupado['count'].astype(int).tolist()
    )
