import pandas as pd
import numpy as np
from django.db.models import Count, Q
from ...models import ConsultaOs, ConsultaEquipamentos
from datetime import datetime


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
        return [], [], [], []

    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], [], [], []

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
    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
    df.dropna(subset=['fechamento'], inplace=True)

    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], [], [], []

    # 4. REMOÇÃO DE DUPLICATAS
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Cálculo das Métricas
    # Cria coluna binária: 1 se Fechada, 0 se não (Aberta, Pendente, etc)
    df['is_fechada'] = (
        (df['situacao'].astype(str).str.lower() == 'fechada') & (df['fechamento'].notnull())
    )
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


def get_taxa_disponibilidade_equipamentos(data_inicio=None, data_fim=None, empresa=None):
    """
    Disponibilidade Geral (%):
    (TotalHorasPossiveis - Downtime) / TotalHorasPossiveis * 100

    TotalHorasPossiveis = 24 * dias_periodo * qtd_equipamentos
    qtd_equipamentos = COUNT DISTINCT tag em ConsultaEquipamentos (parque)
    Downtime = SUM( (fechamento - abertura) em horas ) para OS fechadas no período
              com MENOS DUPLICADOS em (os, tag, local_api)
    """

    # 1) Período (dias) — igual ideia do Looker: min/max do filtro (inclusivo)
    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim)
        dias_periodo = (dt_fim - dt_ini).days + 1
        dt_fim_filter = dt_fim.replace(hour=23, minute=59, second=59)
    else:
        dias_periodo = 30
        dt_ini = None
        dt_fim_filter = None

    # 2) Inventário REAL pelo cadastro de equipamentos
    qs_inv = ConsultaEquipamentos.objects.values('empresa').annotate(
        qtd_equipamentos=Count('tag', distinct=True)
    ).filter(tag__isnull=False).exclude(tag='')

    if empresa:
        qs_inv = qs_inv.filter(empresa=empresa)

    inventario_dict = {
        item['empresa']: item['qtd_equipamentos']
        for item in qs_inv
        if item['empresa']
    }

    if not inventario_dict:
        return [], []

    # 3) Downtime (OS fechadas) — filtrando por ABERTURA como no seu Looker
    qs_os = ConsultaOs.objects.filter(
        situacao__iexact='Fechada',
        abertura__isnull=False,
        fechamento__isnull=False,
    ).values('empresa', 'os', 'tag', 'local_api', 'abertura', 'fechamento')

    if empresa:
        qs_os = qs_os.filter(empresa=empresa)

    df = pd.DataFrame(list(qs_os))
    if df.empty:
        # Sem OS fechada no período => downtime 0 => disponibilidade 100%
        labels = list(inventario_dict.keys())
        valores = [100.0 for _ in labels]
        return labels, valores

    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
    df = df.dropna(subset=['abertura', 'fechamento'])

    if dt_ini is not None:
        df = df[df['abertura'] >= dt_ini]
    if dt_fim_filter is not None:
        df = df[df['abertura'] <= dt_fim_filter]

    if df.empty:
        labels = list(inventario_dict.keys())
        valores = [100.0 for _ in labels]
        return labels, valores

    # MENOS DUPLICADOS (vital para bater com seu filtro do Looker)
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # duração em horas
    df['duracao_h'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['duracao_h'] >= 0]

    downtime_por_empresa = df.groupby('empresa')['duracao_h'].sum().to_dict()

    # 4) Taxa final
    labels = []
    valores = []

    for emp, qtd_equip in inventario_dict.items():
        horas_potenciais = 24 * dias_periodo * qtd_equip
        horas_parado = downtime_por_empresa.get(emp, 0)

        if horas_potenciais > 0:
            taxa = ((horas_potenciais - horas_parado) / horas_potenciais) * 100
        else:
            taxa = 0

        labels.append(emp)
        valores.append(round(taxa, 2))

    return labels, valores


def get_qtde_equipamentos_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna a quantidade de equipamentos cadastrados por unidade.
    Baseado no model ConsultaEquipamentos.
    Filtro de Data: CADASTRO.
    """
    # 1. Busca os dados (Empresa, Tag e Garantia)
    queryset = ConsultaEquipamentos.objects.all().values('empresa', 'tag', 'cadastro')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Tratamento de Data (Baseado na Cadastro)
    df['cadastro'] = pd.to_datetime(df['cadastro'], errors='coerce')

    # Se quiser filtrar apenas quem tem garantia válida no período:
    if data_inicio:
        df = df[df['cadastro'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['cadastro'] <= fim]

    if df.empty:
        return [], []

    # 3. Contagem (Count TAG)
    # Removemos tags vazias para não contar lixo
    df = df[df['tag'].notnull() & (df['tag'] != '')]

    # Remove duplicatas de TAG se houver (para garantir contagem física real)
    df = df.drop_duplicates(subset=['tag'])

    contagem = df['empresa'].value_counts()

    labels = contagem.index.tolist()
    data = contagem.values.tolist()

    return labels, data


def get_idade_media_equipamentos_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula a Idade Média dos equipamentos em Anos.
    Fórmula: (Hoje - Data_Instalacao) / 365.25
    """

    # 1. Busca dados do modelo ConsultaEquipamentos
    # Pegamos 'instalacao' e 'cadastro' (fallback)
    queryset = ConsultaEquipamentos.objects.all().values('empresa', 'instalacao', 'cadastro', 'tag')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Unifica a Data de Referência (Prioridade: Instalação > Cadastro)
    df['instalacao'] = pd.to_datetime(df['instalacao'], errors='coerce')
    df['cadastro'] = pd.to_datetime(df['cadastro'], errors='coerce')

    # Cria coluna 'data_ref' preenchendo instalacao nula com cadastro
    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])

    # Remove quem não tem nenhuma data (não dá pra calcular idade)
    df = df.dropna(subset=['data_ref'])

    # 3. Filtro de Data (Opcional - Geralmente Idade Média é sobre o parque todo ATUAL)
    # Se você quiser filtrar "equipamentos comprados entre data X e Y", descomente abaixo.
    # Mas para "Idade do Parque", geralmente olhamos tudo.
    # if data_inicio:
    #     df = df[df['data_ref'] >= pd.to_datetime(data_inicio)]
    # if data_fim:
    #     fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
    #     df = df[df['data_ref'] <= fim]

    if df.empty:
        return [], []

    # 4. Remove Duplicatas de TAG (para não distorcer a média)
    df = df.drop_duplicates(subset=['tag'])

    # 5. Cálculo da Idade
    hoje = pd.Timestamp.now()
    # Diferença em dias convertida para anos (365.25 considera bissextos)
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25

    # Remove idades negativas (datas futuras erradas) ou absurdas (> 100 anos)
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    # 6. Agrupamento (Média por Empresa)
    df_agrupado = df.groupby('empresa')['idade_anos'].mean().reset_index()

    # Arredonda para 1 casa decimal (Ex: 3.5 anos)
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)

    # Ordena do mais velho para o mais novo
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['idade_anos'].tolist()


def get_idade_media_equipamentos_por_familia(data_inicio=None, data_fim=None, empresa=None):
    """
    Calcula a Idade Média por FAMÍLIA.
    Filtro de Data: Baseado em CADASTRO (conforme pedido).
    Cálculo de Idade: (Hoje - COALESCE(Instalacao, Cadastro)) / 365.25
    """

    # 1. Busca dados
    queryset = ConsultaEquipamentos.objects.all().values('familia', 'instalacao', 'cadastro', 'tag')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Tratamento de Datas
    df['instalacao'] = pd.to_datetime(df['instalacao'], errors='coerce')
    df['cadastro'] = pd.to_datetime(df['cadastro'], errors='coerce')

    # FILTRO DE DATA (Aplica no CADASTRO conforme sua regra)
    # if data_inicio:
    #     df = df[df['cadastro'] >= pd.to_datetime(data_inicio)]
    # if data_fim:
    #     fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
    #     df = df[df['cadastro'] <= fim]

    if df.empty:
        return [], []

    # 3. Define Data de Referência para o cálculo da idade
    # Prioriza Instalação, se não tiver, usa Cadastro
    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])
    df = df.dropna(subset=['data_ref', 'familia'])  # Remove sem data ou sem nome de família

    # 4. Remove Duplicatas de TAG
    df = df.drop_duplicates(subset=['tag'])

    # 5. Cálculo da Idade
    hoje = pd.Timestamp.now()
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25

    # Limpeza de inconsistências
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    # 6. Agrupamento por FAMÍLIA
    df_agrupado = df.groupby('familia')['idade_anos'].mean().reset_index()
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)

    # Ordena do mais velho para o mais novo
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)

    # 7. Limita aos TOP 20 (Para o gráfico não ficar gigante/ilegível)
    # Se quiser todos, remova o .head(20)
    df_agrupado = df_agrupado.head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['idade_anos'].tolist()


def get_maiores_tempos_reparo_criticos_por_familia(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna os Maiores Tempos de Reparo (Média em Horas) por Família.
    BLINDADO CONTRA DUPLICATAS DE OS E DE EQUIPAMENTO.
    """

    # 1. Busca as OS (Fatos)
    qs_os = ConsultaOs.objects.filter(
        tipomanutencao__iexact='CORRETIVA',
        prioridade__icontains='ALTA',
        situacao__iexact='Fechada',
        fechamento__isnull=False,
        abertura__isnull=False,
        tag__isnull=False
    ).exclude(tag='').values('tag', 'abertura', 'fechamento', 'os', 'local_api', 'empresa')

    if empresa:
        qs_os = qs_os.filter(empresa=empresa)

    df_os = pd.DataFrame(list(qs_os))

    if df_os.empty:
        return [], []

    # Tratamento de Datas e Filtro
    df_os['abertura'] = pd.to_datetime(df_os['abertura'], errors='coerce')
    df_os['fechamento'] = pd.to_datetime(df_os['fechamento'], errors='coerce')

    if data_inicio:
        df_os = df_os[df_os['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df_os = df_os[df_os['abertura'] <= fim]

    if df_os.empty:
        return [], []

    # === BLINDAGEM 1: Remove duplicatas de OS ===
    # Garante que cada OS só conte 1 vez
    df_os = df_os.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Cálculo do Tempo
    df_os['horas_reparo'] = (df_os['fechamento'] - df_os['abertura']).dt.total_seconds() / 3600
    df_os = df_os[df_os['horas_reparo'] > 0]  # Remove negativos

    # 2. Busca as Famílias (Dimensão)
    tags_envolvidas = df_os['tag'].unique().tolist()

    qs_equip = ConsultaEquipamentos.objects.filter(
        tag__in=tags_envolvidas
    ).values('tag', 'familia')

    df_equip = pd.DataFrame(list(qs_equip))

    if df_equip.empty:
        return [], []

    # === BLINDAGEM 2: Remove duplicatas de EQUIPAMENTO ===
    # Se a mesma TAG tiver 2 linhas no cadastro, mantemos apenas a primeira encontrada
    # Isso evita o "efeito multiplicador" no Join
    df_equip = df_equip.drop_duplicates(subset=['tag'])

    # 3. Cruzamento
    df_final = pd.merge(df_os, df_equip, on='tag', how='inner')

    if df_final.empty:
        return [], []

    # 4. Agrupamento
    df_agrupado = df_final.groupby('familia')['horas_reparo'].mean().reset_index()

    df_agrupado['horas_reparo'] = df_agrupado['horas_reparo'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_reparo', ascending=False)

    df_agrupado = df_agrupado.head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_reparo'].tolist()


def get_principais_causas_corretivas(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna as Principais Causas de Manutenção Corretiva (Top 10 ou 20).
    Métrica: Contagem de OS (Quantas vezes essa causa ocorreu).
    Filtro: Tipo Manutenção = CORRETIVA.
    """

    # 1. Busca Dados (Filtro CORRETIVA e Fechada/Aberta - geralmente olhamos o histórico todo, mas o padrão é fechada para ter diagnóstico final)
    # DICA: Se a causa for preenchida na abertura, pode pegar abertas também.
    # Vou assumir 'Fechada' para garantir que a causa foi confirmada pelo técnico.
    queryset = ConsultaOs.objects.filter(
        tipomanutencao__iexact='CORRETIVA',
        causa__isnull=False
    ).exclude(causa='').values('causa', 'os', 'tag', 'local_api', 'abertura', 'empresa')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Tratamento de Datas e Filtro
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    # 3. BLINDAGEM: Remove Duplicatas de OS
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 4. Agrupamento e Contagem
    # Conta quantas vezes cada causa aparece
    contagem = df['causa'].value_counts().reset_index()
    contagem.columns = ['causa', 'qtd']

    # 5. Ordenação e Limite
    # O value_counts já ordena do maior para o menor.
    # Pegamos o Top 10 para o gráfico não ficar polúido
    contagem = contagem.head(10)

    return contagem['causa'].tolist(), contagem['qtd'].tolist()


def get_maiores_tempos_parada_criticos_por_familia(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna os Maiores Tempos de Parada (Downtime Médio em Horas) por Família.
    Fórmula: (Funcionamento - Parada).
    Filtros: Corretiva, Crítica, Família válida.
    """

    # 1. Busca as OS (Fatos) com campos de PARADA e FUNCIONAMENTO
    qs_os = ConsultaOs.objects.filter(
        tipomanutencao__iexact='CORRETIVA',
        prioridade__icontains='ALTA',
        # Garante que tem as datas de parada preenchidas
        parada__isnull=False,
        funcionamento__isnull=False,
        tag__isnull=False
    ).exclude(tag='').values('tag', 'parada', 'funcionamento', 'os', 'local_api', 'empresa', 'abertura')

    if empresa:
        qs_os = qs_os.filter(empresa=empresa)

    df_os = pd.DataFrame(list(qs_os))

    if df_os.empty:
        return [], []

    # 2. Tratamento de Datas (Parada e Funcionamento)
    # Abertura usada apenas para filtro de período
    df_os['abertura'] = pd.to_datetime(df_os['abertura'], errors='coerce')
    df_os['parada'] = pd.to_datetime(df_os['parada'], errors='coerce')
    df_os['funcionamento'] = pd.to_datetime(df_os['funcionamento'], errors='coerce')

    # Remove datas inválidas
    df_os = df_os.dropna(subset=['parada', 'funcionamento'])

    # Filtro de Período (Baseado na ABERTURA da OS)
    if data_inicio:
        df_os = df_os[df_os['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df_os = df_os[df_os['abertura'] <= fim]

    if df_os.empty:
        return [], []

    # 3. BLINDAGEM: Remove duplicatas de OS
    df_os = df_os.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 4. Cálculo do Tempo de Parada (Horas)
    df_os['horas_parada'] = (df_os['funcionamento'] - df_os['parada']).dt.total_seconds() / 3600

    # Remove tempos negativos ou zerados (erros de digitação)
    df_os = df_os[df_os['horas_parada'] > 0]

    # 5. Busca as Famílias (Dimensão)
    tags_envolvidas = df_os['tag'].unique().tolist()

    qs_equip = ConsultaEquipamentos.objects.filter(
        tag__in=tags_envolvidas
    ).values('tag', 'familia')

    df_equip = pd.DataFrame(list(qs_equip))

    if df_equip.empty:
        return [], []

    # Remove duplicatas de EQUIPAMENTO
    df_equip = df_equip.drop_duplicates(subset=['tag'])

    # 6. Cruzamento e Filtro de Família
    df_final = pd.merge(df_os, df_equip, on='tag', how='inner')

    # Filtra Família #N/A ou Vazia
    df_final = df_final[
        (df_final['familia'].notnull()) &
        (df_final['familia'] != '') &
        (df_final['familia'] != '#N/A')
    ]

    if df_final.empty:
        return [], []

    # 7. Agrupamento (Média)
    df_agrupado = df_final.groupby('familia')['horas_parada'].mean().reset_index()

    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False)

    # Top 20
    df_agrupado = df_agrupado.head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_parada'].tolist()


def get_tempo_mediano_parada_criticos_por_unidade(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna a MEDIANA do Tempo de Parada (Downtime) por Unidade.
    Filtros: Corretiva, Crítica, Data de Fechamento.
    """

    # 1. Busca as OS (Fatos) com campos de PARADA e FUNCIONAMENTO
    queryset = ConsultaOs.objects.filter(
        tipomanutencao__iexact='CORRETIVA',
        prioridade__icontains='ALTA',
        # Garante que tem as datas necessárias
        parada__isnull=False,
        funcionamento__isnull=False,
        fechamento__isnull=False  # Filtro de data será aqui
    ).values('empresa', 'parada', 'funcionamento', 'fechamento', 'os', 'tag', 'local_api')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Tratamento de Datas
    df['fechamento'] = pd.to_datetime(df['fechamento'], errors='coerce')
    df['parada'] = pd.to_datetime(df['parada'], errors='coerce')
    df['funcionamento'] = pd.to_datetime(df['funcionamento'], errors='coerce')

    # Remove datas inválidas
    df = df.dropna(subset=['parada', 'funcionamento', 'fechamento'])

    # 3. Filtro de Período (Baseado no FECHAMENTO conforme pedido)
    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], []

    # 4. BLINDAGEM: Remove duplicatas de OS
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. Cálculo do Tempo de Parada (Horas)
    df['horas_parada'] = (df['funcionamento'] - df['parada']).dt.total_seconds() / 3600

    # Remove tempos negativos ou zerados
    df = df[df['horas_parada'] > 0]

    if df.empty:
        return [], []

    # 6. Agrupamento (MEDIANA por Empresa)
    # Usamos median() em vez de mean()
    df_agrupado = df.groupby('empresa')['horas_parada'].median().reset_index()

    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['horas_parada'].tolist()


def get_matriz_indisponibilidade_criticos(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna matriz para Heatmap com DETALHAMENTO por empresa no tooltip.
    """

    # 1. Busca os dados
    queryset = ConsultaOs.objects.filter(
        prioridade__icontains='ALTA',
        abertura__isnull=False,
    ).values('os', 'tag', 'local_api', 'abertura', 'empresa')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    dias_ordenados = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    # Função auxiliar para criar estrutura vazia
    def matriz_vazia():
        m = []
        for h in range(24):
            m.append({'hora': f"{h:02d}:00", 'celulas': [{'valor': 0, 'tooltip': ''}] * 7})
        return {'dias': dias_ordenados, 'matriz': m}

    if df.empty:
        return matriz_vazia()

    # 2. Tratamento
    df['abertura'] = pd.to_datetime(df['abertura'], errors='coerce')
    df.dropna(subset=['abertura'], inplace=True)

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return matriz_vazia()

    # 3. MenosDuplicadas
    df = df.sort_values(['os', 'tag', 'local_api', 'abertura'], ascending=[True, True, True, False])
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'], keep='first')

    # 4. Prepara colunas para agrupamento
    df['hora'] = df['abertura'].dt.hour
    df['dia_semana_int'] = df['abertura'].dt.dayofweek  # 0=Seg ... 6=Dom

    # 5. Montagem da Matriz com Detalhamento
    matriz = []

    for h in range(24):
        linha_celulas = []

        # Filtra apenas dados desta hora para ganhar performance no loop dos dias
        df_hora = df[df['hora'] == h]

        for d_int in range(7):
            # Filtra pelo dia da semana dentro daquela hora
            df_slice = df_hora[df_hora['dia_semana_int'] == d_int]
            total = df_slice['os'].nunique()
            tooltip_str = ""

            if total > 0:
                # Conta quantas OS cada empresa teve nesse horário específico
                # Ex: HUGOL: 2, CRER: 1
                contagem_empresas = df_slice.groupby('empresa')['os'].nunique().sort_values(ascending=False)

                # Monta string HTML para o Tooltip: "<b>HUGOL</b>: 2<br><b>CRER</b>: 1"
                lista_detalhes = []
                for emp_nome, emp_qtd in contagem_empresas.items():
                    lista_detalhes.append(f"<b>{emp_nome}</b>: {emp_qtd}")

                tooltip_str = "<br>".join(lista_detalhes)

            linha_celulas.append({
                'valor': total,
                'tooltip': tooltip_str
            })

        matriz.append({
            'hora': f"{h:02d}:00",
            'celulas': linha_celulas  # Lista de objetos {valor, tooltip}
        })

    return {
        'dias': dias_ordenados,
        'matriz': matriz
    }


def get_taxa_disponibilidade_equipamentos_criticos(data_inicio=None, data_fim=None, empresa=None):
    """
    Disponibilidade (%) APENAS para Equipamentos Críticos (Prioridade = ALTA).

    Regra ajustada (correta para disponibilidade):
      - Inventário crítico = histórico (tags distintas que já tiveram prioridade ALTA)
      - Downtime = OS fechada + prioridade ALTA, filtrada por abertura no período
      - MenosDuplicadas = (os, tag, local_api)

    Fórmula:
      ((24 * dias * qtd_equip_criticos) - SUM(TempoParaResolver)) / (24 * dias * qtd_equip_criticos) * 100
    """

    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim)
        dt_fim_filter = dt_fim.replace(hour=23, minute=59, second=59)
        dias_periodo = (dt_fim - dt_ini).days + 1
    else:
        dias_periodo = 30
        dt_ini = None
        dt_fim_filter = None

    # 1) Inventário crítico HISTÓRICO (SEM filtro de data)
    qs_inv = ConsultaOs.objects.filter(
        prioridade__icontains='ALTA',
        tag__isnull=False
    ).exclude(tag='').values('empresa', 'tag')

    if empresa:
        qs_inv = qs_inv.filter(empresa=empresa)

    df_inv = pd.DataFrame(list(qs_inv))
    if df_inv.empty:
        return [], []

    inventario_por_empresa = df_inv.groupby('empresa')['tag'].nunique().to_dict()

    # 2) Downtime (OS críticas fechadas no período por abertura)
    qs_os = ConsultaOs.objects.filter(
        prioridade__icontains='ALTA',
        situacao__iexact='Fechada',
        abertura__isnull=False,
        fechamento__isnull=False
    ).values('empresa', 'os', 'tag', 'local_api', 'abertura', 'fechamento')

    if empresa:
        qs_os = qs_os.filter(empresa=empresa)

    df_os = pd.DataFrame(list(qs_os))
    downtime_por_empresa = {}

    if not df_os.empty:
        df_os['abertura'] = pd.to_datetime(df_os['abertura'], errors='coerce')
        df_os['fechamento'] = pd.to_datetime(df_os['fechamento'], errors='coerce')
        df_os = df_os.dropna(subset=['abertura', 'fechamento'])

        if dt_ini is not None:
            df_os = df_os[df_os['abertura'] >= dt_ini]
        if dt_fim_filter is not None:
            df_os = df_os[df_os['abertura'] <= dt_fim_filter]

        df_os = df_os.drop_duplicates(subset=['os', 'tag', 'local_api'])

        df_os['tempo_resolver'] = (df_os['fechamento'] - df_os['abertura']).dt.total_seconds() / 3600.0
        df_os = df_os[df_os['tempo_resolver'] >= 0]

        downtime_por_empresa = df_os.groupby('empresa')['tempo_resolver'].sum().to_dict()

    # 3) Taxa
    labels, valores = [], []

    for emp, qtd_equip in inventario_por_empresa.items():
        horas_potenciais = 24.0 * dias_periodo * qtd_equip
        horas_parado = float(downtime_por_empresa.get(emp, 0))

        taxa_bruta = ((horas_potenciais - horas_parado) / horas_potenciais) * 100 if horas_potenciais > 0 else 0.0

        if horas_parado > horas_potenciais:
            print(
                f"[ALERTA] {emp} downtime>potencial | "
                f"parado={horas_parado:.2f}h potencial={horas_potenciais:.2f}h "
                f"inventario={qtd_equip} dias={dias_periodo} taxa_bruta={taxa_bruta:.2f}%"
            )

        # clamp BI-safe
        taxa = max(0.0, min(100.0, taxa_bruta))

        labels.append(emp)
        valores.append(round(taxa, 2))

    return labels, valores


def get_qtde_equipamentos_criticos_por_unidade(df_os, df_equip, data_inicio, data_fim, empresa=None):
    """
    Retorna a quantidade de equipamentos CRÍTICOS que foram INSTALADOS no período selecionado,
    agrupados por Unidade (Empresa).

    Lógica:
      1. Identifica tags críticas (baseado no histórico de OS com prioridade ALTA).
      2. Filtra equipamentos pela data de INSTALAÇÃO (data_inicio <= instalacao <= data_fim).
      3. Cruza os dados: Mantém apenas os equipamentos instalados que são críticos.
    """
    if df_os.empty or df_equip.empty:
        return [], []

    # ---------------------------------------------------------
    # 1. Identificar Tags Críticas (Universo Global)
    # ---------------------------------------------------------
    # Olhamos para o df_os completo para saber quais equipamentos são críticos.
    # Não filtramos a OS por data aqui, pois a criticidade é uma característica do equipamento.
    df_o = df_os.copy()

    tags_criticas = []
    if 'prioridade' in df_o.columns and 'tag' in df_o.columns:
        # Busca tags onde a prioridade contém 'ALTA' (case insensitive)
        tags_criticas = df_o[
            df_o['prioridade'].str.upper().str.contains('ALTA', na=False)
        ]['tag'].unique()

    if len(tags_criticas) == 0:
        return [], []

    # ---------------------------------------------------------
    # 2. Filtrar Equipamentos por DATA DE INSTALAÇÃO
    # ---------------------------------------------------------
    df_e = df_equip.copy()

    if 'instalacao' not in df_e.columns:
        return [], []

    # Converte para data
    df_e['instalacao'] = pd.to_datetime(df_e['instalacao'], errors='coerce')

    # Remove quem não tem data de instalação (opcional, mas recomendado para consistência)
    df_e = df_e.dropna(subset=['instalacao'])

    # Aplica o Filtro de Data
    if data_inicio:
        df_e = df_e[df_e['instalacao'] >= pd.to_datetime(data_inicio)]

    if data_fim:
        # Garante o final do dia para a data fim
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df_e = df_e[df_e['instalacao'] <= fim]

    # Filtro de Empresa (se o usuário selecionou uma específica)
    if empresa and 'empresa' in df_e.columns:
        df_e = df_e[df_e['empresa'] == empresa]

    if df_e.empty:
        return [], []

    # ---------------------------------------------------------
    # 3. Cruzamento e Contagem
    # ---------------------------------------------------------
    # Mantém apenas os equipamentos do período (df_e) que estão na lista de críticos
    df_criticos_novos = df_e[df_e['tag'].isin(tags_criticas)]

    if df_criticos_novos.empty:
        return [], []

    # Agrupa por Empresa e Conta
    if 'empresa' in df_criticos_novos.columns:
        agrupado = df_criticos_novos['empresa'].value_counts().reset_index()
        agrupado.columns = ['empresa', 'qtd']

        # Retorna listas para o Chart.js / ApexCharts
        return agrupado['empresa'].tolist(), agrupado['qtd'].tolist()

    return [], []


def get_tempo_primeiro_atendimento_critico(data_inicio=None, data_fim=None, empresa=None):
    """
    Retorna o Tempo Médio para 1º Atendimento (h) de Equipamentos Críticos.
    Fórmula: Data Atendimento - Abertura.
    Filtros: 
      - Corretiva
      - Prioridade Alta
      - Consistência (Atendimento >= Parada)
    """

    # 1. Busca os dados (Filtro: Corretiva e Prioridade Alta)
    queryset = ConsultaOs.objects.filter(
        tipomanutencao__iexact='CORRETIVA',
        prioridade__icontains='ALTA',
        abertura__isnull=False,
        data_atendimento__isnull=False
    ).values('os', 'tag', 'local_api', 'empresa', 'abertura', 'data_atendimento', 'parada')

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return [], []

    # 2. Tratamento de Datas
    cols_data = ['abertura', 'data_atendimento', 'parada']
    for col in cols_data:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Remove datas essenciais inválidas
    df.dropna(subset=['abertura', 'data_atendimento'], inplace=True)

    # 3. Filtro de Período (Baseado na ABERTURA)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    # 4. BLINDAGEM: Menos Duplicadas
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # 5. FILTRO: MenosImediatas (Atendimento deve ser >= Parada)
    # Se a 'parada' estiver preenchida, verificamos a consistência.
    # Se 'parada' for NaT (nula), assumimos que está OK ou filtramos fora dependendo da regra.
    # Assumirei: Se tem parada, atendimento deve ser posterior. Se não tem parada, segue o jogo.

    # Cria uma máscara: Se Parada existe, DataAtendimento >= Parada. Se Parada é NaT, True.
    mask_valid_time = (df['parada'].isnull()) | (df['data_atendimento'] >= df['parada'])
    df = df[mask_valid_time]

    # Filtro extra de sanidade: Atendimento >= Abertura
    df = df[df['data_atendimento'] >= df['abertura']]

    if df.empty:
        return [], []

    # 6. Cálculo da Métrica (Horas)
    df['tempo_atendimento_h'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    # 7. Agrupamento (Média por Empresa)
    df_agrupado = df.groupby('empresa')['tempo_atendimento_h'].mean().reset_index()

    # Arredonda e Ordena
    df_agrupado['tempo_atendimento_h'] = df_agrupado['tempo_atendimento_h'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_atendimento_h', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_atendimento_h'].tolist()
