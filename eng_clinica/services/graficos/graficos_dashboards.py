import pandas as pd
import numpy as np
from datetime import datetime


def get_tempo_medio_atendimento_por_unidade(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []

    # Trabalha com cópia para não afetar o original
    df = df_os.copy()

    # Filtro de Data (Abertura)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    # Cálculo
    df['tempo_horas'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600
    df = df[df['tempo_horas'] >= 0]

    # Agrupamento
    df_agrupado = df.groupby('empresa')['tempo_horas'].mean().reset_index()
    df_agrupado['tempo_horas'] = df_agrupado['tempo_horas'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_horas', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_horas'].tolist()


def get_dispersao_reparo_atendimento(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return []

    df = df_os.copy()

    # Filtro: Situação Fechada
    df = df[df['situacao'].astype(str).str.lower() == 'fechada']

    # Remove sem datas essenciais
    df = df.dropna(subset=['abertura', 'fechamento', 'data_atendimento'])

    # Filtro de Data (Abertura)
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return []

    # Eixos
    df['x'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400  # Dias
    df['y'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600  # Horas

    df = df[(df['x'] >= 0) & (df['y'] >= 0)]
    df = df.sort_values(by='x', ascending=True)

    # Renomeia equipamento para familia para manter compatibilidade com template
    if 'equipamento' in df.columns:
        df = df.rename(columns={'equipamento': 'familia'})
    else:
        df['familia'] = 'N/A'

    return df[['x', 'y', 'empresa', 'familia']].to_dict(orient='records')


def get_tempo_medio_reparo_por_unidade(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []

    df = df_os.copy()

    # Filtro Fechada
    df = df[df['situacao'].astype(str).str.lower() == 'fechada']
    df = df.dropna(subset=['abertura', 'fechamento'])

    # Filtro Data
    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df['tempo_dias'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 86400
    df = df[df['tempo_dias'] >= 0]

    df_agrupado = df.groupby('empresa')['tempo_dias'].mean().reset_index()
    df_agrupado['tempo_dias'] = df_agrupado['tempo_dias'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo_dias', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo_dias'].tolist()


def get_taxa_cumprimento_por_unidade(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], [], [], []

    df = df_os.copy()

    tipos_alvo = ["PREVENTIVA", "CALIBRAÇÃO", "QUALIFICAÇÃO", "TSE"]
    # Filtra tipos (Upper case para garantir)
    df = df[df['tipomanutencao'].astype(str).str.upper().isin(tipos_alvo)]

    df = df.dropna(subset=['abertura'])

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
    df_agrupado['taxa'] = (df_agrupado['sum'] / df_agrupado['count']) * 100
    df_agrupado['taxa'] = df_agrupado['taxa'].round(2)
    df_agrupado = df_agrupado.sort_values(by='taxa', ascending=False)

    return (
        df_agrupado['empresa'].tolist(),
        df_agrupado['taxa'].tolist(),
        df_agrupado['sum'].astype(int).tolist(),
        df_agrupado['count'].astype(int).tolist()
    )


def get_qtde_os_por_tipo_manutencao(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []

    df = df_os.copy()
    df = df.dropna(subset=['abertura'])

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    contagem = df['tipomanutencao'].value_counts()

    return contagem.index.tolist(), contagem.values.tolist()


def get_qtde_os_planejadas_realizadas(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []
    df = df_os.copy()

    # Causa Planejamento E Fechada
    df = df[
        (df['causa'].astype(str).str.upper() == 'PLANEJAMENTO') &
        (df['situacao'].astype(str).str.lower() == 'fechada')
    ]

    # Filtro pela data de FECHAMENTO
    df = df.dropna(subset=['fechamento'])

    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_qtde_os_planejadas_n_realizadas(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []
    df = df_os.copy()

    # Causa Planejamento e NÃO Fechada/Cancelada
    df = df[df['causa'].astype(str).str.upper() == 'PLANEJAMENTO']
    df = df[~df['situacao'].astype(str).str.lower().isin(['fechada', 'cancelada'])]

    # Filtro pela data de ABERTURA
    df = df.dropna(subset=['abertura'])

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_os_taxa_conclusao_planejamento(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], [], [], []
    df = df_os.copy()

    # Planejamento e Não Cancelada
    df = df[df['causa'].astype(str).str.upper() == 'PLANEJAMENTO']
    df = df[df['situacao'].astype(str).str.lower() != 'cancelada']

    # Filtro Data de Fechamento (conforme original)
    df = df.dropna(subset=['fechamento'])  # ATENÇÃO: Se usar fechamento, ignora as abertas.
    # Mas o código original filtrava 'fechamento' no intervalo.
    # Isso significa que só olhamos para as que JÁ FECHARAM no período?
    # Se a lógica for "Taxa de conclusão", deveríamos pegar tudo que foi planejado no período.
    # Vou manter a lógica do original que filtrava `fechamento` no range.

    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], [], [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    df['is_fechada'] = df['situacao'].astype(str).str.lower() == 'fechada'
    df['is_fechada'] = df['is_fechada'].astype(int)

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


def get_taxa_disponibilidade_equipamentos(df_os, df_equip, data_inicio=None, data_fim=None, empresa=None):
    # 1. Período
    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim)
        dias_periodo = (dt_fim - dt_ini).days + 1
        dt_fim_filter = dt_fim.replace(hour=23, minute=59, second=59)
    else:
        dias_periodo = 30
        dt_ini = None
        dt_fim_filter = None

    # 2. Inventário (Baseado no df_equip JÁ FILTRADO na View)
    if df_equip.empty:
        return [], []

    inv_df = df_equip.copy()
    if empresa:
        inv_df = inv_df[inv_df['empresa'] == empresa]

    inventario_dict = inv_df.groupby('empresa')['tag'].nunique().to_dict()

    # 3. Downtime (Baseado no df_os JÁ FILTRADO)
    if df_os.empty:
        downtime_por_empresa = {}
    else:
        df = df_os.copy()
        df = df[df['situacao'].astype(str).str.lower() == 'fechada']
        df = df.dropna(subset=['abertura', 'fechamento'])

        if dt_ini:
            df = df[df['abertura'] >= dt_ini]
        if dt_fim_filter:
            df = df[df['abertura'] <= dt_fim_filter]

        df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
        df['duracao_h'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 3600
        df = df[df['duracao_h'] >= 0]

        downtime_por_empresa = df.groupby('empresa')['duracao_h'].sum().to_dict()

    # 4. Taxa
    labels = []
    valores = []
    for emp, qtd_equip in inventario_dict.items():
        horas_potenciais = 24 * dias_periodo * qtd_equip
        horas_parado = downtime_por_empresa.get(emp, 0)
        taxa = ((horas_potenciais - horas_parado) / horas_potenciais) * 100 if horas_potenciais > 0 else 0
        labels.append(emp)
        valores.append(round(taxa, 2))

    return labels, valores


def get_qtde_equipamentos_por_unidade(df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_equip.empty:
        return [], []
    df = df_equip.copy()

    # Filtro Cadastro
    df = df.dropna(subset=['cadastro'])
    if data_inicio:
        df = df[df['cadastro'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['cadastro'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['tag'])
    contagem = df['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_idade_media_equipamentos_por_unidade(df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_equip.empty:
        return [], []
    df = df_equip.copy()

    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])
    df = df.dropna(subset=['data_ref'])
    df = df.drop_duplicates(subset=['tag'])

    hoje = pd.Timestamp.now()
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    df_agrupado = df.groupby('empresa')['idade_anos'].mean().reset_index()
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['idade_anos'].tolist()


def get_idade_media_equipamentos_por_familia(df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_equip.empty:
        return [], []
    df = df_equip.copy()

    df['data_ref'] = df['instalacao'].fillna(df['cadastro'])
    df = df.dropna(subset=['data_ref', 'familia'])
    df = df.drop_duplicates(subset=['tag'])

    hoje = pd.Timestamp.now()
    df['idade_anos'] = (hoje - df['data_ref']).dt.days / 365.25
    df = df[(df['idade_anos'] >= 0) & (df['idade_anos'] < 100)]

    df_agrupado = df.groupby('familia')['idade_anos'].mean().reset_index()
    df_agrupado['idade_anos'] = df_agrupado['idade_anos'].round(1)
    df_agrupado = df_agrupado.sort_values(by='idade_anos', ascending=False)
    df_agrupado = df_agrupado.head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['idade_anos'].tolist()


def get_maiores_tempos_reparo_criticos_por_familia(df_os, df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty or df_equip.empty:
        return [], []

    # 1. Filtra OS
    dfo = df_os.copy()
    dfo = dfo[
        (dfo['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (dfo['prioridade'].str.upper().str.contains('ALTA', na=False)) &
        (dfo['situacao'].str.lower() == 'fechada')
    ]
    dfo = dfo.dropna(subset=['abertura', 'fechamento'])

    if data_inicio:
        dfo = dfo[dfo['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        dfo = dfo[dfo['abertura'] <= fim]

    dfo = dfo.drop_duplicates(subset=['os', 'tag', 'local_api'])
    dfo['horas_reparo'] = (dfo['fechamento'] - dfo['abertura']).dt.total_seconds() / 3600
    dfo = dfo[dfo['horas_reparo'] > 0]

    # 2. Cruza com Equip (para pegar Familia)
    dfe = df_equip[['tag', 'familia']].copy().drop_duplicates(subset=['tag'])

    df_final = pd.merge(dfo, dfe, on='tag', how='inner')

    if df_final.empty:
        return [], []

    df_agrupado = df_final.groupby('familia')['horas_reparo'].mean().reset_index()
    df_agrupado['horas_reparo'] = df_agrupado['horas_reparo'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_reparo', ascending=False).head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_reparo'].tolist()


def get_principais_causas_corretivas(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []
    df = df_os.copy()

    df = df[df['tipomanutencao'].str.upper() == 'CORRETIVA']
    df = df.dropna(subset=['causa', 'abertura'])
    df = df[df['causa'] != '']

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    contagem = df['causa'].value_counts().head(10).reset_index()
    contagem.columns = ['causa', 'qtd']

    return contagem['causa'].tolist(), contagem['qtd'].tolist()


def get_maiores_tempos_parada_criticos_por_familia(df_os, df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty or df_equip.empty:
        return [], []

    dfo = df_os.copy()
    dfo = dfo[
        (dfo['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (dfo['prioridade'].str.upper().str.contains('ALTA', na=False))
    ]
    dfo = dfo.dropna(subset=['parada', 'funcionamento', 'abertura'])

    if data_inicio:
        dfo = dfo[dfo['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        dfo = dfo[dfo['abertura'] <= fim]

    dfo = dfo.drop_duplicates(subset=['os', 'tag', 'local_api'])
    dfo['horas_parada'] = (dfo['funcionamento'] - dfo['parada']).dt.total_seconds() / 3600
    dfo = dfo[dfo['horas_parada'] > 0]

    dfe = df_equip[['tag', 'familia']].copy().drop_duplicates(subset=['tag'])
    df_final = pd.merge(dfo, dfe, on='tag', how='inner')
    df_final = df_final[df_final['familia'].notnull()]

    if df_final.empty:
        return [], []

    df_agrupado = df_final.groupby('familia')['horas_parada'].mean().reset_index()
    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False).head(20)

    return df_agrupado['familia'].tolist(), df_agrupado['horas_parada'].tolist()


def get_tempo_mediano_parada_criticos_por_unidade(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []
    df = df_os.copy()

    df = df[
        (df['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df['prioridade'].str.upper().str.contains('ALTA', na=False))
    ]
    df = df.dropna(subset=['parada', 'funcionamento', 'fechamento'])

    # Filtro Fechamento
    if data_inicio:
        df = df[df['fechamento'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['fechamento'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    df['horas_parada'] = (df['funcionamento'] - df['parada']).dt.total_seconds() / 3600
    df = df[df['horas_parada'] > 0]

    df_agrupado = df.groupby('empresa')['horas_parada'].median().reset_index()
    df_agrupado['horas_parada'] = df_agrupado['horas_parada'].round(1)
    df_agrupado = df_agrupado.sort_values(by='horas_parada', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['horas_parada'].tolist()


def get_matriz_indisponibilidade_criticos(df_os, data_inicio=None, data_fim=None, empresa=None):
    dias_ordenados = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    def matriz_vazia():
        return {'dias': dias_ordenados, 'matriz': [{'hora': f"{h:02d}:00", 'celulas': [{'valor': 0, 'tooltip': ''}] * 7} for h in range(24)]}

    if df_os.empty:
        return matriz_vazia()

    df = df_os.copy()
    df = df[df['prioridade'].str.upper().str.contains('ALTA', na=False)]
    df = df.dropna(subset=['abertura'])

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return matriz_vazia()

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])
    df['hora'] = df['abertura'].dt.hour
    df['dia_semana_int'] = df['abertura'].dt.dayofweek

    matriz = []
    for h in range(24):
        linha_celulas = []
        df_hora = df[df['hora'] == h]

        for d_int in range(7):
            df_slice = df_hora[df_hora['dia_semana_int'] == d_int]
            total = df_slice['os'].nunique()
            tooltip_str = ""

            if total > 0:
                contagem = df_slice.groupby('empresa')['os'].nunique().sort_values(ascending=False)
                tooltip_str = "<br>".join([f"<b>{emp}</b>: {qtd}" for emp, qtd in contagem.items()])

            linha_celulas.append({'valor': total, 'tooltip': tooltip_str})

        matriz.append({'hora': f"{h:02d}:00", 'celulas': linha_celulas})

    return {'dias': dias_ordenados, 'matriz': matriz}


def get_taxa_disponibilidade_equipamentos_criticos(df_os, df_equip, data_inicio=None, data_fim=None, empresa=None):
    # 1. Período
    if data_inicio and data_fim:
        dt_ini = pd.to_datetime(data_inicio)
        dt_fim = pd.to_datetime(data_fim)
        dias_periodo = (dt_fim - dt_ini).days + 1
        dt_fim_filter = dt_fim.replace(hour=23, minute=59, second=59)
    else:
        dias_periodo = 30
        dt_ini = None
        dt_fim_filter = None

    # 2. Inventário: Baseado em OS históricas de ALTA prioridade (conforme original)
    # Nota: Poderíamos usar o df_equip com alguma coluna de criticidade se existisse, mas o original usa OS.
    # Mas atenção: O df_os que chega aqui JÁ É FILTRADO por Equipamento Médico.
    if df_os.empty:
        return [], []

    df_inv = df_os.copy()
    df_inv = df_inv[df_inv['prioridade'].str.upper().str.contains('ALTA', na=False)]

    inventario_dict = df_inv.groupby('empresa')['tag'].nunique().to_dict()

    # 3. Downtime
    df_down = df_inv.copy()  # Já é Alta prioridade
    df_down = df_down[df_down['situacao'].str.lower() == 'fechada']
    df_down = df_down.dropna(subset=['abertura', 'fechamento'])

    if dt_ini:
        df_down = df_down[df_down['abertura'] >= dt_ini]
    if dt_fim_filter:
        df_down = df_down[df_down['abertura'] <= dt_fim_filter]

    downtime_por_empresa = {}
    if not df_down.empty:
        df_down = df_down.drop_duplicates(subset=['os', 'tag', 'local_api'])
        df_down['tempo'] = (df_down['fechamento'] - df_down['abertura']).dt.total_seconds() / 3600
        df_down = df_down[df_down['tempo'] >= 0]
        downtime_por_empresa = df_down.groupby('empresa')['tempo'].sum().to_dict()

    labels, valores = [], []
    for emp, qtd in inventario_dict.items():
        potencial = 24 * dias_periodo * qtd
        parado = downtime_por_empresa.get(emp, 0)
        taxa = ((potencial - parado) / potencial) * 100 if potencial > 0 else 0
        labels.append(emp)
        valores.append(round(max(0, min(100, taxa)), 2))

    return labels, valores


def get_qtde_equipamentos_criticos_por_unidade(df_os, df_equip, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty or df_equip.empty:
        return [], []

    # Identifica Tags Críticas (pelo histórico de OS)
    tags_criticas = df_os[df_os['prioridade'].str.upper().str.contains('ALTA', na=False)]['tag'].unique()

    if len(tags_criticas) == 0:
        return [], []

    # Filtra Equipamentos
    dfe = df_equip.copy()
    dfe = dfe.dropna(subset=['instalacao'])

    if data_inicio:
        dfe = dfe[dfe['instalacao'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        dfe = dfe[dfe['instalacao'] <= fim]

    dfe = dfe[dfe['tag'].isin(tags_criticas)]

    if dfe.empty:
        return [], []

    contagem = dfe['empresa'].value_counts()
    return contagem.index.tolist(), contagem.values.tolist()


def get_tempo_primeiro_atendimento_critico(df_os, data_inicio=None, data_fim=None, empresa=None):
    if df_os.empty:
        return [], []
    df = df_os.copy()

    df = df[
        (df['tipomanutencao'].str.upper() == 'CORRETIVA') &
        (df['prioridade'].str.upper().str.contains('ALTA', na=False))
    ]
    df = df.dropna(subset=['abertura', 'data_atendimento'])

    if data_inicio:
        df = df[df['abertura'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)
        df = df[df['abertura'] <= fim]

    if df.empty:
        return [], []

    df = df.drop_duplicates(subset=['os', 'tag', 'local_api'])

    # Validação de consistencia com parada
    mask = (df['parada'].isnull()) | (df['data_atendimento'] >= df['parada'])
    df = df[mask]
    df = df[df['data_atendimento'] >= df['abertura']]

    df['tempo'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    df_agrupado = df.groupby('empresa')['tempo'].mean().reset_index()
    df_agrupado['tempo'] = df_agrupado['tempo'].round(2)
    df_agrupado = df_agrupado.sort_values(by='tempo', ascending=False)

    return df_agrupado['empresa'].tolist(), df_agrupado['tempo'].tolist()
