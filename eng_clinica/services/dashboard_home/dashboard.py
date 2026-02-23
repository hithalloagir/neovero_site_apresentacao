import pandas as pd


def get_evolucao_backlog_metrologia(df_merged):
    """
    Gráfico - Pendências totais de metrologia atrasadas (temporal)
    Recebe df_merged que já é o Inner Join de OS com Equipamentos Médicos.
    """
    if df_merged is None or df_merged.empty:
        return [], []

    df = df_merged.copy()

    # 2. Remove OSs canceladas PRIMEIRO
    if 'situacao' in df.columns:
        df = df[~df['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO', 'FECHADA'])]

    # 3. Filtro das "Planejadas"
    if 'tipomanutencao' in df.columns:
        termos_planejadas = [
            'CALIBRA',
            'QUALIFICA',
            'TSE',
            'ENSAIO',
            'SEGURANÇA ELÉTRICA'
        ]
        regex = '|'.join(termos_planejadas)
        df = df[
            df['tipomanutencao'].str.upper().str.contains(regex, na=False, regex=True)
        ]

    if df.empty:
        return [], []

    # 🔥 4. DEDUPLICAÇÃO CORRETA: Por (OS + Empresa + API)
    # Cria uma chave única combinando os 3 campos
    df['chave_unica'] = (
        df['os'].astype(str) + '|' +
        df['empresa'].fillna('').astype(str) + '|' +
        df['local_api'].fillna('').astype(str)
    )

    # Para cada combinação única, agregamos os dados
    df_deduplicated = df.groupby('chave_unica', as_index=False).agg({
        'os': 'first',
        'empresa': 'first',
        'local_api': 'first',
        'abertura': 'min',              # Data de abertura mais antiga
        'fechamento': lambda x: x.max() if x.notna().all() else pd.NaT,  # Se alguma está aberta, NaT
        'situacao': 'last',             # Situação mais recente
        'tipomanutencao': 'first',
        'tag': 'first'
    })

    # Remove a chave auxiliar
    df = df_deduplicated.drop('chave_unica', axis=1)

    # 5. Filtro temporal (últimos 24 meses)
    hoje = pd.Timestamp.now()

    # Define o limite como o último dia do mês passado
    ultimo_dia_mes_passado = (hoje.replace(day=1) - pd.Timedelta(seconds=1))

    # Filtramos dados de 12 meses antes do mês passado para garantir o histórico
    limite_historico = hoje - pd.DateOffset(months=24)
    df = df[df['abertura'] >= limite_historico]

    # 6. Definir janela de tempo (Ajustado para 12 meses exatos)

    # Define o fim como o primeiro dia do mês passado (Janeiro/2026)
    fim_periodo = (hoje.replace(day=1) - pd.DateOffset(months=1))

    # Mudado de 11 para 11 meses atrás + o mês atual = 12 meses
    inicio_periodo = (fim_periodo - pd.DateOffset(months=11)).replace(day=1, hour=0, minute=0, second=0)
    mes_atual = hoje.replace(day=1, hour=0, minute=0, second=0)

    lista_meses = pd.date_range(
        start=inicio_periodo,
        end=fim_periodo,
        freq='MS'
    )

    labels = []
    data_saldo = []

    # 7. Cálculo do Passivo Mensal
    for mes_inicio in lista_meses:
        # Último instante do mês
        proximo_mes = mes_inicio + pd.DateOffset(months=1)
        corte = proximo_mes - pd.Timedelta(seconds=1)

        # OSs que estavam abertas naquela data
        passivo_no_mes = df[
            (df['abertura'] <= corte) &
            ((df['fechamento'].isna()) | (df['fechamento'] > corte))
        ]

        qtd_acumulada = len(passivo_no_mes)

        mes_nome = mes_inicio.strftime('%m/%Y')
        labels.append(mes_nome)
        data_saldo.append(qtd_acumulada)

    return labels, data_saldo


def get_evolucao_backlog_manutencoes_corretivas(df_merged):
    """
    Gráfico - Pendencias de manutenção corretiva
    Recebe df_merged que já é o Inner Join de OS com Equipamentos Médicos.
    """
    if df_merged is None or df_merged.empty:
        return [], []

    df = df_merged.copy()
    try:
        # ---------------------------------------------------------
        # PROCESSAMENTO DO BACKLOG
        # ---------------------------------------------------------

        # Remove canceladas
        if 'situacao' in df.columns:
            df = df[~df['situacao'].str.upper().isin(['FECHADA', 'CANCELADA', 'INATIVAÇÃO'])]

        # Filtro de Data Recente (últimos 12 meses) e Tipo Corretiva
        hoje = pd.Timestamp.now()
        limite_atraso = hoje - pd.DateOffset(months=24)

        if 'tipomanutencao' in df.columns:
            df = df[
                (df['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)) &
                (df['abertura'] >= limite_atraso)
            ]

        if df.empty:
            return [], []

        # Deduplicação
        df['chave_unica'] = (
            df['os'].astype(str) + '|' +
            df['empresa'].fillna('').astype(str) + '|' +
            df['local_api'].fillna('').astype(str)
        )

        df = df.groupby('chave_unica', as_index=False).agg({
            'os': 'first',
            'abertura': 'min',
            'fechamento': lambda x: x.max() if x.notna().all() else pd.NaT
        })

        # Janela de Tempo
        fim_grafico = (hoje.replace(day=1) - pd.DateOffset(months=1))
        inicio_grafico = (fim_grafico - pd.DateOffset(months=11))

        lista_meses = pd.date_range(start=inicio_grafico, end=fim_grafico, freq='MS')

        labels = []
        data_saldo = []

        for mes_inicio in lista_meses:
            proximo_mes = mes_inicio + pd.DateOffset(months=1)
            corte = proximo_mes - pd.Timedelta(seconds=1)

            passivo = df[
                (df['abertura'] <= corte) &
                ((df['fechamento'].isna()) | (df['fechamento'] > corte))
            ]

            labels.append(mes_inicio.strftime('%m/%Y'))
            data_saldo.append(len(passivo))

        return labels, data_saldo

    except Exception as e:
        print(f"❌ Erro crítico ao gerar gráfico de corretivas: {e}")
        # Em caso de qualquer erro não previsto, retorna vazio para não quebrar a página
        return [], []


def get_total_servicos_realizados(df_merged):
    """
    Gráfico - Eficiência (Abertas e Fechadas no mesmo mês)
    Recebe df_merged que já é o Inner Join de OS com Equipamentos Médicos.
    """
    if df_merged is None or df_merged.empty:
        return [], []

    df = df_merged.copy()

    # Remove linhas sem data
    df = df.dropna(subset=['fechamento', 'abertura'])

    # Filtra Status (Remove Canceladas)
    if 'situacao' in df.columns:
        df = df[~df['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO', 'ABERTA', 'PENDENTE'])]

    # ---------------------------------------------------------
    # 4. DEDUPLICAÇÃO (Regra de Ouro)
    # ---------------------------------------------------------
    df['chave_unica'] = (
        df['os'].astype(str) + '|' +
        df['empresa'].fillna('').astype(str) + '|' +
        df['local_api'].fillna('').astype(str)
    )

    # Agrupa pegando os extremos de data para cada OS
    df = df.groupby('chave_unica', as_index=False).agg({
        'abertura': 'min',
        'fechamento': 'max'
    })

    # ---------------------------------------------------------
    # 5. LÓGICA DE EFICIÊNCIA (SEM LOOP DE DATA)
    # ---------------------------------------------------------

    # Criamos colunas auxiliares com o formato "YYYY-MM"
    # Isso ignora dias e horas. Se é Dezembro, é Dezembro.
    df['mes_abertura'] = df['abertura'].dt.to_period('M')
    df['mes_fechamento'] = df['fechamento'].dt.to_period('M')

    # AQUI ESTÁ A CORREÇÃO:
    # Filtra onde o mês de abertura é IGUAL ao mês de fechamento
    df_eficiencia = df[df['mes_abertura'] == df['mes_fechamento']]

    # ---------------------------------------------------------
    # 6. MONTAGEM DO GRÁFICO (12 Meses)
    # ---------------------------------------------------------
    hoje = pd.Timestamp.now()
    fim_periodo = (hoje.replace(day=1) - pd.DateOffset(months=1)).to_period('M')
    inicio_periodo = (fim_periodo - 11)  # Volta 11 meses

    # Cria a lista de meses completa (PeriodIndex)
    todos_meses = pd.period_range(start=inicio_periodo, end=fim_periodo, freq='M')

    # Conta quantas OSs tem em cada mês de fechamento
    contagem = df_eficiencia.groupby('mes_fechamento').size()

    # Alinha com a lista completa de meses (preenche zero onde não tem nada)
    contagem_final = contagem.reindex(todos_meses, fill_value=0)

    # Prepara saída
    labels = [p.strftime('%m/%Y') for p in contagem_final.index]
    data_total = contagem_final.values.tolist()

    return labels, data_total


def get_quantidade_equipamentos_cadastrados(df_equip_medicos):
    """
    KPI - Quantidade Total de Equipamentos Médicos
    Recebe df_equip_medicos já filtrado na View.
    Retorna: int (Ex: 150)
    """
    # 1. Validação: Se não tiver dados, retorna 0 direto
    if df_equip_medicos is None or df_equip_medicos.empty:
        return 0

    # 4. Retorna o tamanho do dataframe filtrado (inteiro)
    return len(df_equip_medicos)


def get_disponibilidade_total(df_merged, df_equip_medicos):
    """
    KPI - Disponibilidade Total
    Lógica: (Total Equipamentos Médicos) - (Equipamentos em Corretiva com Parada Aberta)
    Retorna: percentual (float), qtd_disponivel (int), qtd_total (int)
    """
    # 1. Validação Básica
    if df_equip_medicos is None or df_equip_medicos.empty:
        return 0.0, 0, 0

    total_equip = len(df_equip_medicos)

    # ---------------------------------------------------------
    # PASSO B: CALCULAR EQUIPAMENTOS PARADOS (NUMERADOR NEGATIVO)
    # ---------------------------------------------------------
    if df_merged is None or df_merged.empty:
        # Se não tem OS, disponibilidade é 100%
        return 100.0, total_equip, total_equip

    df_filtrada = df_merged.copy()

    qtd_parados = 0

    # === A LÓGICA DE "PARADO" ===
    # 1. Tipo Manutenção contém 'CORRETIVA'
    # 2. Data de Parada NÃO é Nula (Teve parada)
    # 3. Data de Fechamento É Nula (Ainda não voltou/não fechou a OS)
    # 4. Situação não é Cancelada

    filtro_parado = (
        (df_filtrada['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)) &
        (df_filtrada['parada'].notna()) &  # Tem data de parada
        (df_filtrada['fechamento'].isna()) &  # Não tem data de volta (fechamento)
        (~df_filtrada['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO']))
    )

    # Contamos as TAGS ÚNICAS paradas (para não contar 2x se tiver duplicidade de mão de obra)
    equipamentos_parados = df_filtrada[filtro_parado]['tag'].nunique()
    qtd_parados = equipamentos_parados

    # ---------------------------------------------------------
    # PASSO C: CÁLCULO FINAL
    # ---------------------------------------------------------
    qtd_disponivel = total_equip - qtd_parados

    pct_disponibilidade = (qtd_disponivel / total_equip) * 100

    return round(pct_disponibilidade, 2), qtd_disponivel, total_equip


def get_detalhes_equipamentos_parados(df_merged):
    """
    Retorna lista de equipamentos parados para o AG Grid.
    Correção: Adicionado drop_duplicates(subset=['os']) para simular o DISTINCT ON.
    """
    if df_merged is None or df_merged.empty:
        return []

    df_filtrada = df_merged.copy()

    filtro_parado = (
        (df_filtrada['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)) &
        (df_filtrada['parada'].notna()) &
        (df_filtrada['fechamento'].isna()) &
        (~df_filtrada['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO']))
    )

    df_parados = df_filtrada[filtro_parado].copy()

    if df_parados.empty:
        return []

    # =========================================================
    # 5. DEDUPLICAÇÃO (A CORREÇÃO ESTÁ AQUI)
    # =========================================================
    # Isso faz o mesmo que "SELECT DISTINCT ON (os.os)"
    # Ordenamos primeiro para garantir consistência
    df_parados = df_parados.sort_values(by=['os'])

    # Remove duplicatas mantendo a primeira ocorrência da OS
    df_parados = df_parados.drop_duplicates(subset=['os'], keep='first')

    # =========================================================

    # 6. Cálculos Finais e Formatação
    hoje = pd.Timestamp.now()

    # Dias parado
    df_parados['dias_parado'] = (hoje - df_parados['parada']).dt.days

    # Formatação de Data
    df_parados['data_parada_fmt'] = df_parados['parada'].dt.strftime('%d/%m/%Y %H:%M')

    # Preenche modelo vazio se necessário
    if 'modelo' in df_parados.columns:
        df_parados['modelo'] = df_parados['modelo'].fillna('-')
    else:
        df_parados['modelo'] = '-'

    # Seleção final de colunas
    cols_final = [
        'os', 'empresa', 'tag', 'tipoequipamento', 'modelo',
        'data_parada_fmt', 'dias_parado', 'tipomanutencao', 'situacao'
    ]
    cols_existentes_final = [c for c in cols_final if c in df_parados.columns]

    # Retorna ordenado por dias parado (maior para menor)
    return df_parados[cols_existentes_final].sort_values('dias_parado', ascending=False).to_dict('records')


def get_equipamentos_criticos_indisponiveis_os(df_merged):
    """
    KPI - Quantidade de Equipamentos Críticos Parados
    Lógica: Equipamentos Médicos com OS Corretiva + Parada + Aberta + Prioridade ALTA
    Retorna: int (Quantidade absoluta)
    """
    if df_merged is None or df_merged.empty:
        return 0

    df_filtrada = df_merged.copy()

    # Normaliza a Prioridade
    if 'prioridade' in df_filtrada.columns:
        df_filtrada['prioridade'] = df_filtrada['prioridade'].astype(str).str.strip().str.upper()

    qtd_criticos_parados = 0

    # === LÓGICA DE CRÍTICO PARADO ===
    # Prioridade ALTA + Corretiva + Parado + Sem Volta
    filtro_critico = (
        (df_filtrada['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)) &
        (df_filtrada['parada'].notna()) &
        (df_filtrada['fechamento'].isna()) &
        (~df_filtrada['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO'])) &
        (df_filtrada['prioridade'] == 'ALTA')  # <--- O filtro chave
    )

    # Conta quantos equipamentos únicos estão nessa situação
    qtd_criticos_parados = df_filtrada[filtro_critico]['tag'].nunique()

    return qtd_criticos_parados


def get_detalhes_equipamentos_criticos_indisponiveis(df_merged):
    """
    Retorna lista de equipamentos criticos indisponiveis para o AG Grid.
    Correção: Adicionado drop_duplicates(subset=['os']) para simular o DISTINCT ON.
    """
    if df_merged is None or df_merged.empty:
        return []

    df_filtrada = df_merged.copy()

    filtro_parado = (
        (df_filtrada['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)) &
        (df_filtrada['parada'].notna()) &
        (df_filtrada['fechamento'].isna()) &
        (~df_filtrada['situacao'].str.upper().isin(['CANCELADA', 'INATIVAÇÃO'])) &
        (df_filtrada['prioridade'] == 'ALTA')  # <--- O filtro chave para críticos
    )

    df_parados = df_filtrada[filtro_parado].copy()

    if df_parados.empty:
        return []

    # =========================================================
    # 5. DEDUPLICAÇÃO (A CORREÇÃO ESTÁ AQUI)
    # =========================================================
    # Isso faz o mesmo que "SELECT DISTINCT ON (os.os)"
    # Ordenamos primeiro para garantir consistência
    df_parados = df_parados.sort_values(by=['os'])

    # Remove duplicatas mantendo a primeira ocorrência da OS
    df_parados = df_parados.drop_duplicates(subset=['os'], keep='first')

    # =========================================================

    # 6. Cálculos Finais e Formatação
    hoje = pd.Timestamp.now()

    # Dias parado
    df_parados['dias_parado'] = (hoje - df_parados['parada']).dt.days

    # Formatação de Data
    df_parados['data_parada_fmt'] = df_parados['parada'].dt.strftime('%d/%m/%Y %H:%M')

    # Preenche modelo vazio se necessário
    if 'modelo' in df_parados.columns:
        df_parados['modelo'] = df_parados['modelo'].fillna('-')
    else:
        df_parados['modelo'] = '-'

    # Seleção final de colunas
    cols_final = [
        'os', 'empresa', 'tag', 'tipoequipamento', 'modelo',
        'data_parada_fmt', 'dias_parado', 'tipomanutencao', 'situacao',
        'prioridade',
    ]
    cols_existentes_final = [c for c in cols_final if c in df_parados.columns]

    # Retorna ordenado por dias parado (maior para menor)
    return df_parados[cols_existentes_final].sort_values('dias_parado', ascending=False).to_dict('records')


def get_mtbf_por_familia_aggrid(df_merged, df_equip_medicos):
    """
    Retorna os dados de MTBF por Família para o AG Grid.
    Calcula a idade desde a Instalação/Cadastro e usa TODAS as corretivas fechadas.
    """
    if df_equip_medicos is None or df_equip_medicos.empty:
        return []

    # 1. Base de Equipamentos (O Universo)
    df_e = df_equip_medicos.copy()

    familias_validas = [
        "ADAPTADOR ENDOSCOPIO", "ANALISADOR DE GASES RESPIRATÓRIOS", "APARELHO DE ANESTESIA",
        "APARELHO DE ASPIRAÇÃO DE SECREÇÃO COMPACTO", "APARELHO DE FOTOTERAPIA", "APARELHO DE PRESSAO",
        "ASPIRADOR", "AUTOCLAVE", "BALANCA", "BERCO AQUECIDO", "BISTURI ELETRICO", "BOMBA DE INFUSAO",
        "BOMBA INFUSAO", "CAPNOGRAFO", "CARDIOVERSOR", "CAMA HOSPITALAR", "CPAP", "DESFIBRILADOR",
        "ELETROCARDIOGRAFO", "ENDOSCOPIO", "ESFIGMOMANOMETRO", "FOCO CIRURGICO", "FOTOTERAPIA",
        "HEMODIALISE", "INCUBADORA", "LARINGOSCOPIO", "MARCAPASSO", "MESA CIRURGICA", "MONITOR",
        "MONITOR MULTIPARAMETRICO", "MONITOR PACIENTE", "NEBULIZADOR", "OXIMETRO", "OTOSCOPIO",
        "OFTALMOSCOPIO", "RAIO X", "RESPIRADOR", "TOMOGRAFO", "ULTRASSOM", "VENTILADOR",
        "VENTILADOR PULMONAR", "VENTILADOR PULMONAR DE TRANSPORTE", "VENTILADOR TRANSPORTE",
        "VECTOELETRONISTAMOGRAFO"
    ]

    df_e = df_e[df_e['familia'].isin(familias_validas)]

    if df_e.empty:
        return []

    # Prepara as datas para calcular a idade
    if 'instalacao' in df_e.columns and 'cadastro' in df_e.columns:
        df_e['instalacao'] = pd.to_datetime(df_e['instalacao'], errors='coerce')
        df_e['cadastro'] = pd.to_datetime(df_e['cadastro'], errors='coerce')
        df_e['data_ref'] = df_e['instalacao'].fillna(df_e['cadastro'])
    else:
        return []

    # Remove o que não tem data ou não tem família
    df_e = df_e.dropna(subset=['data_ref', 'tag', 'familia'])
    df_e = df_e[df_e['familia'] != '']
    df_e = df_e.drop_duplicates(subset=['tag'])

    # Calcula dias de vida até hoje
    hoje = pd.Timestamp.now()
    df_e['dias_vida'] = (hoje - df_e['data_ref']).dt.days
    df_e = df_e[df_e['dias_vida'] >= 0]  # Remove dados inconsistentes (datas no futuro)

    # Agrupa por Família para saber o potencial total
    df_fam = df_e.groupby('familia').agg(
        qtd_equipamentos=('tag', 'count'),
        total_dias_vida=('dias_vida', 'sum')
    ).reset_index()

    # 2. Filtrar as Fato (Ordens de Serviço)
    if df_merged is not None and not df_merged.empty:
        df_o = df_merged.copy()
        df_o = df_o.dropna(subset=['abertura', 'fechamento'])

        # Filtros de Regra: Corretiva + Fechada
        if 'tipomanutencao' in df_o.columns:
            df_o = df_o[df_o['tipomanutencao'].str.upper().str.contains('CORRETIVA', na=False)]
        if 'situacao' in df_o.columns:
            df_o = df_o[df_o['situacao'].str.upper() == 'FECHADA']

        df_o = df_o.drop_duplicates(subset=['os', 'tag', 'local_api'])

        # Merge para garantir que a OS pertence a um equipamento médico e pegar a Família
        df_o_fam = pd.merge(df_o, df_e[['tag', 'familia']], on='tag', how='inner')

        # Tempo Parado (em dias)
        df_o_fam['downtime_dias'] = (df_o_fam['fechamento'] - df_o_fam['abertura']).dt.total_seconds() / 86400
        df_o_fam = df_o_fam[df_o_fam['downtime_dias'] >= 0]

        # Agrupa as OSs por família
        os_agrupado = df_o_fam.groupby('familia').agg(
            total_os=('os', 'count'),
            total_downtime=('downtime_dias', 'sum')
        ).reset_index()

        # Junta os equipamentos com as OSs
        df_fam = pd.merge(df_fam, os_agrupado, on='familia', how='left')

    # 3. Preenche as famílias que NUNCA quebraram com zeros
    if 'total_os' not in df_fam.columns:
        df_fam['total_os'] = 0
        df_fam['total_downtime'] = 0
    else:
        df_fam['total_os'] = df_fam['total_os'].fillna(0)
        df_fam['total_downtime'] = df_fam['total_downtime'].fillna(0)

    # 4. O Cálculo Final do MTBF (TMEF)
    # Disponibilidade = Total de Vida - Total Parado
    df_fam['disponibilidade'] = df_fam['total_dias_vida'] - df_fam['total_downtime']
    df_fam.loc[df_fam['disponibilidade'] < 0, 'disponibilidade'] = 0

    import numpy as np
    # Se total_os > 0, MTBF = Disponibilidade / OS
    # Se NUNCA quebrou, o MTBF atual é igual à média de idade da frota daquela família
    df_fam['mtbf_dias'] = np.where(
        df_fam['total_os'] > 0,
        df_fam['disponibilidade'] / df_fam['total_os'],
        df_fam['total_dias_vida'] / df_fam['qtd_equipamentos']
    )

    df_fam['mtbf_dias'] = df_fam['mtbf_dias'].round(1)

    # Ordena para mostrar as piores famílias (MTBF Menor) no topo da tabela
    df_fam = df_fam.sort_values('mtbf_dias', ascending=True)
    print(df_fam[['familia', 'qtd_equipamentos', 'total_os', 'total_dias_vida', 'total_downtime', 'disponibilidade', 'mtbf_dias']])

    return df_fam[['familia', 'qtd_equipamentos', 'total_os', 'mtbf_dias']].to_dict('records')
