
import pandas as pd
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
    # OTIMIZAÇÃO: Filtramos no banco ANTES de criar o DataFrame
    # Como o formato é YYYY-MM-DD, a comparação de string funciona no SQL
    queryset = ConsultaOs.objects.all().values(
        'abertura', 'fechamento', 'data_atendimento', 'empresa', 'equipamento'
    )

    if empresa:
        queryset = queryset.filter(empresa=empresa)

    # Filtro de Data no Nível do Banco (String Comparison)
    # Isso evita carregar dados de 2020 se você só quer 2025
    if data_inicio:
        queryset = queryset.filter(abertura__gte=str(data_inicio))

    if data_fim:
        # Garante que pegue até o final da string do dia se for apenas YYYY-MM-DD
        queryset = queryset.filter(abertura__lte=f"{str(data_fim)} 23:59:59")

    # Só agora carregamos para a memória
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return []

    # ... (O restante do seu código de conversão pd.to_datetime continua igual) ...
    # ... Mas agora ele vai processar muito menos linhas! ...

    # 2. Conversão de Datas
    cols_data = ['abertura', 'fechamento', 'data_atendimento']
    for col in cols_data:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    df = df.dropna(subset=cols_data)

    # 4. Cálculos das Métricas
    df['x'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 3600 / 24
    df['y'] = (df['data_atendimento'] - df['abertura']).dt.total_seconds() / 3600

    # 5. Limpeza e Ordenação
    df = df[(df['x'] >= 0) & (df['y'] >= 0)]

    # LIMITADOR DE PERFORMANCE PARA O GRÁFICO
    # Se tiver 5.000 bolinhas, o navegador trava. Vamos limitar aos últimos 1000 ou fazer uma amostra.
    if len(df) > 1000:
        df = df.sort_values(by='abertura', ascending=False).head(1000)

    df['x'] = df['x'].round(2)
    df['y'] = df['y'].round(2)

    df = df.sort_values(by='x', ascending=True)

    df = df.rename(columns={'equipamento': 'familia'})
    dados_grafico = df[['x', 'y', 'empresa', 'familia']].to_dict(orient='records')

    return dados_grafico
