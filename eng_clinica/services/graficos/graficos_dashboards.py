import pandas as pd
import numpy as np

# ==============================================================================
# GRÁFICOS DE ORDENS DE SERVIÇO (OS)
# ==============================================================================


def get_tempo_medio_atendimento_por_unidade(df_os):
    """
    Calcula Tempo Médio de Atendimento (Abertura -> Atendimento).
    """
    if df_os.empty:
        return [], []

    # 1. Copia e Garante Datas
    df = df_os.dropna(subset=['abertura', 'data_atendimento']).copy()

    if df.empty:
        return [], []

    # 2. CÁLCULO PRELIMINAR (Antes de remover duplicatas)
    # Precisamos calcular agora para poder filtrar os negativos antes de escolher a linha única
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    # 3. FILTRO DE CONSISTÊNCIA (Igual ao WHERE do SQL)
    # Remove tempos negativos AGORA. Assim, se uma OS tem uma linha ruim e uma boa, sobra a boa.
    df = df[df['tempo_horas'] >= 0]

    if df.empty:
        return [], []

    # 4. ORDENAÇÃO (Determinística)
    # Garante que, se sobrarem 2 linhas válidas para a mesma OS, pegamos a mesma que o SQL pegaria
    # (SQL usa ORDER BY os, tag, local_api, abertura DESC)
    df = df.sort_values(by=['os', 'tag', 'local_api', 'abertura'], ascending=[True, True, True, False])

    # 5. REMOVE DUPLICATAS
    # Agora sim, com os dados limpos e ordenados, pegamos a linha única
    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'], keep='first')

    # === AUDITORIA (Pode remover depois) ===
    print("\n" + "=" * 50)
    print("AUDITORIA PYTHON (CORRIGIDO): TEMPO MÉDIO ATENDIMENTO")
    print(df['empresa'].value_counts())
    print("=" * 50 + "\n")
    # =======================================

    # 6. Agrupamento Final
    df_agrupado = df.groupby('empresa')['tempo_horas'].mean().reset_index()
    df_agrupado['tempo_horas'] = df_agrupado['tempo_horas'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_horas', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_horas'].tolist()


def get_dispersao_reparo_atendimento(df_os):
    """
    Scatter Plot: Reparo (Dias) x Atendimento (Horas).
    Filtro Implícito: Apenas OS Fechadas (pois precisa de data fechamento).
    """
    if df_os.empty:
        return []

    # Filtra Fechadas e com datas válidas
    df = df_os[
        (df_os['situacao'].str.lower() == 'fechada') &
        (df_os['abertura'].notnull()) &
        (df_os['fechamento'].notnull()) &
        (df_os['data_atendimento'].notnull())
    ].copy()

    if df.empty:
        return []

    # Cálculos
    # Eixo X: Dias | Eixo Y: Horas
    df['x'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400  # Dias
    df['y'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600  # Horas

    # Remove inconsistências
    df = df[(df['x'] >= 0) & (df['y'] >= 0)]

    # Formatação para o Chart.js
    df = df.sort_values(by='x', ascending=True)

    # Renomeia coluna 'equipamento' para 'familia' se necessário, ou usa equipamento mesmo
    # O original usava 'equipamento' na query e renomeava para 'familia' no DF
    if 'equipamento' in df.columns:
        df['familia'] = df['equipamento']
    else:
        df['familia'] = 'N/A'

    return df[['x', 'y', 'empresa', 'familia']].to_dict(orient='records')


def get_tempo_medio_reparo_por_unidade(df_os):
    """
    Calcula Tempo Médio de Reparo (Abertura -> Fechamento).
    """
    if df_os.empty:
        return [], []

    df = df_os[
        (df_os['situacao'].str.lower() == 'fechada') &
        (df_os['fechamento'].notnull()) &
        (df_os['abertura'].notnull())
    ].copy()

    if df.empty:
        return [], []

    df['tempo_dias'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400
    df = df[df['tempo_dias'] >= 0]

    df_agrupado = df.groupby('empresa')['tempo_dias'].mean().reset_index()
    df_agrupado['tempo_dias'] = df_agrupado['tempo_dias'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_dias', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_dias'].tolist()


def get_taxa_cumprimento_por_unidade(df_os):
    """
    Taxa de Cumprimento (%) para PREV, CALIB, QUALI e TSE.
    """
    if df_os.empty:
        return [], [], [], []

    tipos_alvo = ["PREVENTIVA", "CALIBRAÇÃO", "QUALIFICAÇÃO", "TSE"]

    # Filtra tipos (Case Insensitive force)
    # Assumindo que tipomanutencao vem padronizado ou aplicamos str.upper()
    df = df_os[df_os['tipomanutencao'].str.upper().isin(tipos_alvo)].copy()

    if df.empty:
        return [], [], [], []

    # Cria flag de fechada
    df['is_fechada'] = df['situacao'].astype(str).str.lower() == 'fechada'
    df['is_fechada'] = df['is_fechada'].astype(int)

    df_agrupado = df.groupby('empresa')['is_fechada'].agg(['sum', 'count']).reset_index()

    # Cálculo da Taxa
    df_agrupado['taxa'] = (df_agrupado['sum'] / df_agrupado['count']) * 100
    df_agrupado['taxa'] = df_agrupado['taxa'].round(2)
    df_agrupado = df_agrupado.sort_values(by='taxa', ascending=False)

    return (
        df_agrupado['empresa'].tolist(),
        df_agrupado['taxa'].tolist(),
        df_agrupado['sum'].astype(int).tolist(),
        df_agrupado['count'].astype(int).tolist()
    )


def get_qtde_os_por_tipo_manutencao(df_os):
    """
    Contagem de OS por Tipo.
    """
    if df_os.empty:
        return [], []

    # Remove duplicatas de OS se houver múltiplas linhas para mesma OS
    # (Importante se a consulta original trazia joins que duplicavam)
    df = df_os.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['tipomanutencao'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_qtde_os_planejadas_realizadas(df_os):
    """
    Planejadas (Causa=Planejamento) e Fechadas.
    """
    if df_os.empty:
        return [], []

    df = df_os[
        (df_os['causa'].str.upper() == 'PLANEJAMENTO') &
        (df_os['situacao'].str.lower() == 'fechada')
    ].copy()

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_qtde_os_planejadas_n_realizadas(df_os):
    """
    Planejadas Pendentes (Não Fechadas e Não Canceladas).
    """
    if df_os.empty:
        return [], []

    df = df_os[
        (df_os['causa'].str.upper() == 'PLANEJAMENTO') &
        (~df_os['situacao'].str.lower().isin(['fechada', 'cancelada']))
    ].copy()

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_os_taxa_conclusao_planejamento(df_os):
    """
    % Conclusão de Planejamento (Exclui Canceladas).
    """
    if df_os.empty:
        return [], [], [], []

    # Filtra Universo Planejamento (Sem canceladas)
    df = df_os[
        (df_os['causa'].str.upper() == 'PLANEJAMENTO') &
        (df_os['situacao'].str.lower() != 'cancelada')
    ].copy()

    if df.empty:
        return [], [], [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Flag Fechada
    df['is_fechada'] = (df['situacao'].str.lower() == 'fechada').astype(int)

    df_agrupado = df.groupby('empresa')['is_fechada'].agg(['sum', 'count']).reset_index()

    df_agrupado['taxa'] = (df_agrupado['sum'] / df_agrupado['count']) * 100
    df_agrupado['taxa'] = df_agrupado['taxa'].round(2)
    df_agrupado = df_agrupado.sort_values(by='taxa', ascending=False)

    return (
        df_agrupado['empresa'].tolist(),
        df_agrupado['taxa'].tolist(),
        df_agrupado['sum'].astype(int).tolist(),
        df_agrupado['count'].astype(int).tolist()
    )


def get_taxa_disponibilidade_equipamentos(df_os):
    """
    Calcula Disponibilidade Geral.
    NOTA: Usa o df_os para estimar o inventário (tags únicas que tiveram OS).
    Se quiser usar inventário total cadastrado, precisaria passar df_equip.
    Vou manter a lógica original (baseada em OS) para consistência.
    """
    if df_os.empty:
        return [], []

    # 1. Inventário Dinâmico (Tags únicas no período/filtro)
    # Se df_os já vem filtrado por data, isso pega apenas equipamentos ativos no período.
    inventario_por_empresa = df_os.groupby('empresa')['tag'].nunique().to_dict()

    if not inventario_por_empresa:
        return [], []

    # 2. Período (Dias)
    # Estima o delta T com base nas datas do dataframe para não depender de inputs externos
    # Ou fixa em 30 dias se for o padrão.
    if not df_os['abertura'].empty:
        max_date = df_os['abertura'].max()
        min_date = df_os['abertura'].min()
        dias_periodo = (max_date - min_date).days + 1
        if dias_periodo < 1:
            dias_periodo = 1
    else:
        dias_periodo = 30

    # 3. Downtime (Horas Parado) - Apenas OS Fechadas
    df_closed = df_os[
        (df_os['situacao'].str.lower() == 'fechada') &
        (df_os['fechamento'].notnull()) &
        (df_os['abertura'].notnull())
    ].copy()

    df_closed['duracao_s'] = (df_closed['fechamento'] - df_closed['abertura']).dt.total_seconds()
    df_closed = df_closed[df_closed['duracao_s'] >= 0]

    downtime_por_empresa = df_closed.groupby('empresa')['duracao_s'].sum().to_dict()

    # 4. Cálculo Final
    labels = []
    valores = []

    for nome_empresa, qtd_equip in inventario_por_empresa.items():
        # Horas Totais (24h * Dias * Qtd Equipamentos)
        horas_potenciais = 24 * dias_periodo * qtd_equip

        # Horas Parado (converte segundos para horas)
        horas_parado = downtime_por_empresa.get(nome_empresa, 0) / 3600

        taxa = 0
        if horas_potenciais > 0:
            taxa = ((horas_potenciais - horas_parado) / horas_potenciais) * 100

        labels.append(nome_empresa)
        valores.append(round(taxa, 2))

    return labels, valores


def get_principais_causas_corretivas(df_os):
    """
    Top Causas de Corretivas.
    """
    if df_os.empty:
        return [], []

    df = df_os[
        (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df_os['causa'].notnull()) &
        (df_os['causa'] != '')
    ].copy()

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    contagem = df['causa'].value_counts().head(10)
    return contagem.index.tolist(), contagem.values.tolist()


def get_tempo_mediano_parada_criticos_por_unidade(df_os):
    """
    Mediana de Parada (Funcionamento - Parada) para Críticos.
    """
    if df_os.empty:
        return [], []

    # Filtros: Corretiva, Crítica, Datas válidas
    df = df_os[
        (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df_os['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (df_os['parada'].notnull()) &
        (df_os['funcionamento'].notnull())
    ].copy()

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    df['horas_parada'] = (df['funcionamento'] - df['parada']).dt.total_seconds() / 3600
    df = df[df['horas_parada'] > 0]

    df_agrupado = df.groupby('empresa')['horas_parada'].median().reset_index()
    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['horas_parada'].tolist()


def get_matriz_indisponibilidade_criticos(df_os):
    """
    Heatmap de OS Críticas por Hora/Dia.
    """
    # Estrutura padrão vazia
    dias_ordenados = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    def matriz_vazia():
        m = []
        for h in range(24):
            m.append({'hora': f"{h:02d}:00", 'celulas': [{'valor': 0, 'tooltip': ''}] * 7})
        return {'dias': dias_ordenados, 'matriz': m}

    if df_os.empty:
        return matriz_vazia()

    # Filtro Críticas
    df = df_os[
        (df_os['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (df_os['abertura'].notnull())
    ].copy()

    if df.empty:
        return matriz_vazia()

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Extrai Hora e Dia da Semana
    df['hora'] = df['abertura'].dt.hour
    df['dia_semana_int'] = df['abertura'].dt.dayofweek

    matriz = []
    for h in range(24):
        linha_celulas = []
        df_hora = df[df['hora'] == h]

        for d_int in range(7):
            df_slice = df_hora[df_hora['dia_semana_int'] == d_int]
            total = len(df_slice)
            tooltip_str = ""

            if total > 0:
                contagem_empresas = df_slice['empresa'].value_counts()
                lista_detalhes = [f"<b>{emp}</b>: {qtd}" for emp, qtd in contagem_empresas.items()]
                tooltip_str = "<br>".join(lista_detalhes)

            linha_celulas.append({'valor': total, 'tooltip': tooltip_str})

        matriz.append({'hora': f"{h:02d}:00", 'celulas': linha_celulas})

    return {'dias': dias_ordenados, 'matriz': matriz}


def get_taxa_disponibilidade_equipamentos_criticos(df_os):
    """
    Disponibilidade para Críticos (Prioridade ALTA).
    """
    if df_os.empty:
        return [], []

    # 1. Inventário Crítico (Tags únicas com histórico ALTA neste DF)
    df_criticos = df_os[df_os['prioridade'].str.upper().str.contains('ALTA', na=False)].copy()

    if df_criticos.empty:
        return [], []

    inventario_por_empresa = df_criticos.groupby('empresa')['tag'].nunique().to_dict()

    # 2. Período
    max_date = df_os['abertura'].max()
    min_date = df_os['abertura'].min()
    dias_periodo = (max_date - min_date).days + 1
    if dias_periodo < 1:
        dias_periodo = 1

    # 3. Downtime Crítico (Fechadas)
    df_closed = df_criticos[
        (df_criticos['situacao'].str.lower() == 'fechada') &
        (df_criticos['fechamento'].notnull()) &
        (df_criticos['abertura'].notnull())
    ].copy()

    df_closed = df_closed.drop_duplicates(subset=['os', 'tag', 'local_api'])
    df_closed['duracao_s'] = (df_closed['fechamento'] - df_closed['abertura']).dt.total_seconds()
    df_closed = df_closed[df_closed['duracao_s'] >= 0]

    downtime_por_empresa = df_closed.groupby('empresa')['duracao_s'].sum().to_dict()

    labels = []
    valores = []

    for nome_empresa, qtd_equip in inventario_por_empresa.items():
        horas_potenciais = 24 * dias_periodo * qtd_equip
        horas_parado = downtime_por_empresa.get(nome_empresa, 0) / 3600

        taxa = 0
        if horas_potenciais > 0:
            taxa = ((horas_potenciais - horas_parado) / horas_potenciais) * 100

        labels.append(nome_empresa)
        valores.append(round(taxa, 2))

    return labels, valores


def get_tempo_primeiro_atendimento_critico(df_os):
    """
    Tempo 1º Atendimento (Abertura -> Data Atendimento) para Críticos.
    """
    if df_os.empty:
        return [], []

    df = df_os[
        (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df_os['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (df_os['abertura'].notnull()) &
        (df_os['data_atendimento'].notnull())
    ].copy()

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Filtro de consistência: Atendimento >= Parada (se parada existir)
    # Se parada for NaT, considera válido.
    condicao_parada = (df['parada'].isnull()) | (df['data_atendimento'] >= df['parada'])
    df = df[condicao_parada]

    df['tempo_h'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    # Consistência básica: não pode ter atendido antes de abrir
    df = df[df['tempo_h'] >= 0]

    df_agrupado = df.groupby('empresa')['tempo_h'].mean().reset_index()
    df_agrupado['tempo_h'] = df_agrupado['tempo_h'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_h', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_h'].tolist()


# ==============================================================================
# GRÁFICOS DE EQUIPAMENTOS (Consomem df_equip)
# ==============================================================================

def get_qtde_equipamentos_por_unidade(df_equip):
    """
    Contagem de Equipamentos Cadastrados (Count TAGs).
    """
    if df_equip.empty:
        return [], []

    # Conta apenas tags válidas
    df = df_equip[df_equip['tag'].notnull() & (df_equip['tag'] != '')].copy()

    # Remove duplicatas de tag para contagem real
    df = df.drop_duplicates(subset=['tag'])

    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_idade_media_equipamentos_por_unidade(df_equip):
    """
    Idade Média (Hoje - Instalação/Cadastro).
    """
    if df_equip.empty:
        return [], []

    df = df_equip.copy()

    # Unifica Data Ref
    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])
    df = df.dropna(subset=['data_ref'])

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['tag'])

    hoje = pd.Timestamp.now()
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    df_agrupado = df.groupby('empresa')['idade_anos'].mean().reset_index()
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['idade_anos'].tolist()


def get_idade_media_equipamentos_por_familia(df_equip):
    """
    Idade Média por Família.
    """
    if df_equip.empty:
        return [], []

    df = df_equip.dropna(subset=['familia']).copy()

    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])
    df = df.dropna(subset=['data_ref'])

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['tag'])

    hoje = pd.Timestamp.now()
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    df_agrupado = df.groupby('familia')['idade_anos'].mean().reset_index()
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)

    # Top 20 para visualização
    df_agrupado = df_agrupado.head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['idade_anos'].tolist()


# ==============================================================================
# GRÁFICOS MISTOS (JOIN OS + EQUIP)
# ==============================================================================

def get_maiores_tempos_reparo_criticos_por_familia(df_os, df_equip):
    """
    Join OS + Equipamento para pegar Família Correta.
    """
    if df_os.empty or df_equip.empty:
        return [], []

    # 1. Filtra OS Crítica e Corretiva
    df_o = df_os[
        (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df_os['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (df_os['situacao'].str.lower() == 'fechada') &
        (df_os['tag'].notnull())
    ].copy()

    if df_o.empty:
        return [], []

    df_o = df_o.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Cálculo horas
    df_o['horas_reparo'] = (df_o['fechamento'] - df_o['abertura']).dt.total_seconds() / 3600
    df_o = df_o[df_o['horas_reparo'] > 0]

    # 2. Prepara Equipamento
    df_e = df_equip[['tag', 'familia']].dropna().drop_duplicates(subset=['tag'])

    # 3. Join
    df_merged = pd.merge(df_o, df_e, on='tag', how='inner')

    if df_merged.empty:
        return [], []

    df_agrupado = df_merged.groupby('familia')['horas_reparo'].mean().reset_index()
    df_agrupado['horas_reparo'] = df_agrupado['horas_reparo'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_reparo', ascending=False).head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_reparo'].tolist()


def get_maiores_tempos_parada_criticos_por_familia(df_os, df_equip):
    """
    Join OS + Equip para Parada Crítica.
    """
    if df_os.empty or df_equip.empty:
        return [], []

    df_o = df_os[
        (df_os['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df_os['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (df_os['parada'].notnull()) &
        (df_os['funcionamento'].notnull()) &
        (df_os['tag'].notnull())
    ].copy()

    if df_o.empty:
        return [], []

    df_o = df_o.drop_duplicates(subset=['os', 'tag', 'local_api'])
    df_o['horas_parada'] = (df_o['funcionamento'] - df_o['parada']).dt.total_seconds() / 3600
    df_o = df_o[df_o['horas_parada'] > 0]

    df_e = df_equip[['tag', 'familia']].dropna().drop_duplicates(subset=['tag'])

    # Filtra famílias inválidas
    df_e = df_e[~df_e['familia'].isin(['#N/A', ''])]

    df_merged = pd.merge(df_o, df_e, on='tag', how='inner')

    if df_merged.empty:
        return [], []

    df_agrupado = df_merged.groupby('familia')['horas_parada'].mean().reset_index()
    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False).head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_parada'].tolist()


def get_qtde_equipamentos_criticos_por_unidade(df_os, df_equip):
    """
    Conta equipamentos na tabela Equip que têm histórico ALTA na tabela OS.
    """
    if df_os.empty or df_equip.empty:
        return [], []

    # 1. Pega tags críticas do DF OS
    tags_criticas = df_os[
        df_os['prioridade'].str.upper().str.contains('ALTA', na=False)
    ]['tag'].unique()

    if len(tags_criticas) == 0:
        return [], []

    # 2. Filtra DF Equip
    df_e = df_equip[df_equip['tag'].isin(tags_criticas)].copy()

    # Se quiser aplicar filtro de data na Garantia/Instalação, deve ser feito no df_equip antes
    # ou assumir que o df_equip passado já está no contexto desejado.

    df_e = df_e.drop_duplicates(subset=['tag'])

    contagem = df_e['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()
