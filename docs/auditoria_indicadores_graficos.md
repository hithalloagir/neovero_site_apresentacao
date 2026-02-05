# Auditoria de Indicadores e Gráficos

## Sumário
| Nome | Tipo (Indicador/Gráfico) | Página | Fonte | Arquivo principal |
| --- | --- | --- | --- | --- |
| Equipamentos Cadastrados | Indicador | /eng_clinica/indicadores/ | consulta_equipamentos | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Manutenção Corretiva | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| MTBF Médio | Indicador | /eng_clinica/indicadores/ | consulta_equipamentos + consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| MTTR (Dias) | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Reparos Imediatos | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Tempo 1º Atendimento | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Mediana 1º Atendimento | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| TMA Crítico (Alta Prioridade) | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Mediana 1º Atendimento Crítico | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Downtime Médio Crítico | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Mediana Tempo Equipamento Parado | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Taxa de Disponibilidade | Indicador | /eng_clinica/indicadores/ | consulta_os + consulta_equipamentos | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Disp. Equip. Críticos | Indicador | /eng_clinica/indicadores/ | consulta_os + consulta_equipamentos | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Equipamentos Indisponíveis | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Críticos Indisponíveis | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| % Resolução no Período | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Pendências / Equip. | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Cumprimento Preventiva | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Cumprimento Calibração | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Cumprimento Treinamento | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Cumprimento TSE | Indicador | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Maiores Causas de Corretivas | Indicador (tabela) | /eng_clinica/indicadores/ | consulta_os | eng_clinica/services/indicadores/indicadores_dashboards.py |
| OS Corretivas por Família | Indicador (tabela) | /eng_clinica/indicadores/ | consulta_os + consulta_equipamentos | eng_clinica/services/indicadores/indicadores_dashboards.py |
| Tempo médio de atendimento por unidade (h) | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Tempo de Reparo x Tempo de Atendimento | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Tempo médio de reparo por unidade (dia) | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Quantidade de OS por Tipo de Manutenção | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Taxa de cumprimento de prev, calib, quali e TSE (%) | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Quantidade de OS planejadas já realizadas | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Quantidade de OS planejadas não fechadas | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Porcentagem de OS Planejadas Concluídas | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Taxa de Disponibilidade Geral dos Equipamentos | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Taxa de Disponibilidade dos Equipamentos Críticos | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Qtde de Equipamentos Cadastrados por Unidade | Gráfico | /eng_clinica/graficos/ | consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Qtde de Equipamentos Críticos por Unidade | Gráfico | /eng_clinica/graficos/ | consulta_os + consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Tempo 1º Atendimento Equip. Crítico (h) | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Idade Média dos Equipamentos por Unidade (Anos) | Gráfico | /eng_clinica/graficos/ | consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Idade dos Equipamentos por Família (Anos) - Top 20 | Gráfico | /eng_clinica/graficos/ | consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Maiores tempos de reparo de equipamentos críticos por família (h) | Gráfico | /eng_clinica/graficos/ | consulta_os + consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Principais Causas de Corretivas | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Maiores tempos de PARADA de equipamentos críticos por família (h) | Gráfico | /eng_clinica/graficos/ | consulta_os + consulta_equipamentos | eng_clinica/services/graficos/graficos_dashboards.py |
| Tempo MEDIANO de Parada de Críticos por Unidade (h) | Gráfico | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |
| Horários em que equipamentos críticos ficaram indisponíveis | Gráfico (heatmap) | /eng_clinica/graficos/ | consulta_os | eng_clinica/services/graficos/graficos_dashboards.py |

## Mapa geral do pipeline
As rotas do módulo estão em `eng_clinica/urls.py:6-8`. As views `engenharia_clinica_indicadores` e `engenharia_clinica_graficos` leem `data_inicio`, `data_fim` e `empresa` via GET, com padrão início do mês até hoje, e usam `GraficoFilterForm` (eng_clinica/forms.py:5-24). Os dados vêm das tabelas `consulta_os` e `consulta_equipamentos` via models `ConsultaOs` e `ConsultaEquipamentos` (eng_clinica/models.py:4-108). Na view de indicadores, as consultas são executadas uma única vez e carregadas em DataFrames (eng_clinica/views.py:414-448); os KPIs são calculados em `eng_clinica/services/indicadores/indicadores_dashboards.py`. Na view de gráficos, cada função consulta o banco diretamente (eng_clinica/services/graficos/graficos_dashboards.py), embora a view também carregue DataFrames que não são usados no cálculo (eng_clinica/views.py:99-144). Os gráficos usam `json_script` no template (eng_clinica/templates/engenharia/graficos.html:438-505) e são renderizados em Chart.js (dashboard_graficos_charts.js; Chart.js carregado em templates/base.html:69-70).
Regras gerais: conversão de datas com `pd.to_datetime(..., errors='coerce')`, remoção de NaT, filtros por período geralmente em `abertura` ou `fechamento`, deduplicação por (`os`,`tag`,`local_api`) ou por `tag`, exclusão de tags vazias e tempos negativos. Não há normalização explícita de timezone; todos os cálculos usam timestamps ingênuos do pandas.

⚠️ Riscos e hipóteses: a view de gráficos carrega `df_os`/`df_equip` mas os serviços fazem novas queries (custo duplicado); o script `dashboard_indicadores_charts.js` é incluído no template, porém não há `<canvas>` nem `json_script` na página de indicadores; o uso de datas como texto em `consulta_os` exige cast/conversão consistente e pode introduzir desvios se houver timezone ou formatos fora do padrão.

## Indicadores
### Equipamentos Cadastrados
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:40`.
- **Fonte de dados:** tabela `consulta_equipamentos` (model `ConsultaEquipamentos`).
- **Definição (negócio):** quantidade de equipamentos únicos cadastrados no período selecionado.
- **Fórmula:** `COUNT(DISTINCT tag)` após limpeza de tags.
- **Campos/tabelas:** `consulta_equipamentos.tag`, `consulta_equipamentos.cadastro`, `consulta_equipamentos.empresa`.
- **Filtros:** `cadastro` entre `data_inicio` e `data_fim` (inclusive); filtro opcional por `empresa`.
- **Regras de limpeza e tratamento:** conversão de `cadastro` para datetime; remoção de `tag` nula/vazia; deduplicação por `tag`.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:7-46.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-448.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:40.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT COUNT(DISTINCT tag) AS total_equipamentos
FROM consulta_equipamentos
WHERE tag IS NOT NULL
  AND tag <> ''
  AND (:empresa IS NULL OR empresa = :empresa)
  AND cadastro >= :data_inicio::timestamp
  AND cadastro <= (:data_fim::timestamp + interval '23:59:59');
```
- **Validações de consistência sugeridas:** comparar com total de tags cadastradas no período por empresa; validar duplicidade de tag no cadastro; checar cadastros fora do intervalo.

### Manutenção Corretiva
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:80`.
- **Fonte de dados:** tabela `consulta_os` (model `ConsultaOs`).
- **Definição (negócio):** total de OS corretivas fechadas no período.
- **Fórmula:** `COUNT(*)` de OS corretivas fechadas, com deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.os`, `consulta_os.tag`, `consulta_os.local_api`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`, `consulta_os.empresa`.
- **Filtros:** `fechamento` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; filtro opcional por `empresa`.
- **Regras de limpeza e tratamento:** conversão de `fechamento`; remoção de datas inválidas; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:47-92.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:80.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT COUNT(*) AS total_os_corretivas
FROM base
WHERE fechamento IS NOT NULL
  AND fechamento >= :data_inicio::timestamp
  AND fechamento <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA';
```
- **Validações de consistência sugeridas:** reconciliar com contagem de OS corretivas fechadas no período; checar duplicidade por (`os`,`tag`,`local_api`); verificar OS sem fechamento.

### MTBF Médio
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:119`.
- **Fonte de dados:** tabelas `consulta_equipamentos` e `consulta_os`.
- **Definição (negócio):** média do MTBF em anos por equipamento (idade / número de falhas corretivas), usando idade desde instalação (ou cadastro) até hoje.
- **Fórmula:** para cada tag, `idade_anos / qtd_falhas`; se `qtd_falhas = 0`, usa `idade_anos`; retorna a média das tags.
- **Campos/tabelas:** `consulta_equipamentos.tag`, `consulta_equipamentos.instalacao`, `consulta_equipamentos.cadastro`; `consulta_os.tag`, `consulta_os.tipomanutencao`.
- **Filtros:** filtro opcional por `empresa`; sem filtro de período para falhas.
- **Regras de limpeza e tratamento:** ignora equipamentos sem `instalacao` e `cadastro`; idade negativa vira 0; conta falhas corretivas sem deduplicação.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:157-210.
- **Trechos do código (Backend - query):** eng_clinica/views.py:439-448 (equipamentos) e eng_clinica/services/indicadores/indicadores_dashboards.py:171-183 (consulta de falhas).
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:119.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim (não aplicados ao cálculo no código)
WITH equip AS (
    SELECT tag,
           COALESCE(instalacao, cadastro) AS data_ref
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL
      AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
),
falhas AS (
    SELECT tag, COUNT(*) AS qtd_falhas
    FROM consulta_os
    WHERE UPPER(tipomanutencao) = 'CORRETIVA'
      AND tag IS NOT NULL
      AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
    GROUP BY tag
),
calc AS (
    SELECT e.tag,
           EXTRACT(EPOCH FROM (NOW() - e.data_ref)) / (365.25 * 86400) AS idade_anos,
           COALESCE(f.qtd_falhas, 0) AS qtd_falhas
    FROM equip e
    LEFT JOIN falhas f ON f.tag = e.tag
    WHERE e.data_ref IS NOT NULL
)
SELECT ROUND(AVG(CASE WHEN qtd_falhas = 0 THEN idade_anos ELSE idade_anos / qtd_falhas END), 1) AS mtbf_medio_anos
FROM calc
WHERE idade_anos >= 0;
```
- **Validações de consistência sugeridas:** conferir se tags sem falhas entram com MTBF = idade; verificar se a contagem de falhas deveria ser deduplicada; validar idades negativas e equipamentos sem data.

### MTTR (Dias)
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:152`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** tempo médio de reparo (dias) para OS corretivas fechadas no período.
- **Fórmula:** `AVG(fechamento - abertura)` em dias, após deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`, `consulta_os.os`, `consulta_os.tag`, `consulta_os.local_api`.
- **Filtros:** `fechamento` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`.
- **Regras de limpeza e tratamento:** conversão de datas; remoção de tempos negativos; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:211-277.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:152.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (fechamento - abertura)) / 86400.0), 2) AS mttr_dias
FROM base
WHERE abertura IS NOT NULL
  AND fechamento IS NOT NULL
  AND fechamento >= :data_inicio::timestamp
  AND fechamento <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND fechamento >= abertura;
```
- **Validações de consistência sugeridas:** comparar com MTTR calculado em BI/SQL direto; checar OS com fechamento anterior à abertura; validar efeito de deduplicação.

### Reparos Imediatos
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:185`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** quantidade de OS corretivas com duração de reparo menor que 1 minuto.
- **Fórmula:** `COUNT(*)` de OS com `(fechamento - abertura) < 60s`, após deduplicação.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`, `consulta_os.os`, `consulta_os.tag`, `consulta_os.local_api`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`.
- **Regras de limpeza e tratamento:** remove registros sem `fechamento`; remove duração negativa; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1304-1357.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:185.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT COUNT(*) AS reparos_imediatos
FROM base
WHERE abertura IS NOT NULL
  AND fechamento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND EXTRACT(EPOCH FROM (fechamento - abertura)) BETWEEN 0 AND 59.999;
```
- **Validações de consistência sugeridas:** revisar OS com duração < 1 minuto; checar se há fechamentos automáticos; validar deduplicação.

### Tempo 1º Atendimento
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:221`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** tempo médio até o primeiro atendimento (horas) para OS fechadas no período.
- **Fórmula:** `AVG(data_atendimento - abertura)` em horas.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.data_atendimento`, `consulta_os.situacao`, `consulta_os.ocorrencia`, `consulta_os.data_chamado`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `situacao = 'fechada'`; `ocorrencia != 'ATIVIDADE PROGRAMADA'`; `data_chamado` não nula.
- **Regras de limpeza e tratamento:** conversão de datas; remove tempos negativos; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:278-347.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:221.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(data_atendimento, '')::timestamp AS data_atendimento,
        NULLIF(data_chamado, '')::timestamp AS data_chamado,
        situacao,
        ocorrencia,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (data_atendimento - abertura)) / 3600.0), 2) AS tempo_medio_h
FROM base
WHERE abertura IS NOT NULL
  AND data_atendimento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND LOWER(situacao) = 'fechada'
  AND (UPPER(COALESCE(ocorrencia, '')) <> 'ATIVIDADE PROGRAMADA')
  AND data_chamado IS NOT NULL
  AND data_atendimento >= abertura;
```
- **Validações de consistência sugeridas:** comparar média com mediana; verificar OS sem `data_chamado`; checar ocorrências “ATIVIDADE PROGRAMADA”.

### Mediana 1º Atendimento
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:254`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** mediana do tempo para primeiro atendimento (horas).
- **Fórmula:** `MEDIAN(data_atendimento - abertura)` em horas.
- **Campos/tabelas:** mesmos do indicador “Tempo 1º Atendimento”.
- **Filtros:** mesmos do indicador “Tempo 1º Atendimento”.
- **Regras de limpeza e tratamento:** conversão de datas; remove tempos negativos; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:348-404.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:254.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(data_atendimento, '')::timestamp AS data_atendimento,
        NULLIF(data_chamado, '')::timestamp AS data_chamado,
        situacao,
        ocorrencia,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (data_atendimento - abertura)) / 3600.0)
, 2) AS mediana_h
FROM base
WHERE abertura IS NOT NULL
  AND data_atendimento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND LOWER(situacao) = 'fechada'
  AND (UPPER(COALESCE(ocorrencia, '')) <> 'ATIVIDADE PROGRAMADA')
  AND data_chamado IS NOT NULL
  AND data_atendimento >= abertura;
```
- **Validações de consistência sugeridas:** garantir que a mediana seja <= média quando há outliers; verificar quantidade mínima de OS válidas.

### TMA Crítico (Alta Prioridade)
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:287`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** tempo médio para 1º atendimento em OS corretivas de alta prioridade (críticas).
- **Fórmula:** `AVG(data_atendimento - abertura)` em horas.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.data_atendimento`, `consulta_os.tipomanutencao`, `consulta_os.prioridade`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”.
- **Regras de limpeza e tratamento:** conversão de datas; remove tempos negativos; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:405-464.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:287.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(data_atendimento, '')::timestamp AS data_atendimento,
        tipomanutencao,
        prioridade,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (data_atendimento - abertura)) / 3600.0), 2) AS tempo_medio_h
FROM base
WHERE abertura IS NOT NULL
  AND data_atendimento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND data_atendimento >= abertura;
```
- **Validações de consistência sugeridas:** validar se todas as OS críticas possuem `data_atendimento`; conferir se há prioridade “ALTA” com grafia diferente.

### Mediana 1º Atendimento Crítico
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:320`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** mediana do tempo de 1º atendimento para OS críticas.
- **Fórmula:** `MEDIAN(data_atendimento - abertura)` em horas.
- **Campos/tabelas:** mesmos do indicador “TMA Crítico”.
- **Filtros:** mesmos do indicador “TMA Crítico”.
- **Regras de limpeza e tratamento:** conversão de datas; remove tempos negativos; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:465-520.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:320.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(data_atendimento, '')::timestamp AS data_atendimento,
        tipomanutencao,
        prioridade,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (data_atendimento - abertura)) / 3600.0)
, 2) AS mediana_h
FROM base
WHERE abertura IS NOT NULL
  AND data_atendimento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND data_atendimento >= abertura;
```
- **Validações de consistência sugeridas:** garantir tamanho mínimo da amostra; comparar com média para detectar outliers.

### Downtime Médio Crítico
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:353`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** tempo médio em horas que equipamentos críticos ficaram parados (downtime) no período.
- **Fórmula:** `AVG(funcionamento - parada)` em horas.
- **Campos/tabelas:** `consulta_os.parada`, `consulta_os.funcionamento`, `consulta_os.tipomanutencao`, `consulta_os.prioridade`, `consulta_os.abertura`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”.
- **Regras de limpeza e tratamento:** remove OS sem `parada`/`funcionamento`; remove tempos negativos; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:521-589.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:353.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(parada, '')::timestamp AS parada,
        NULLIF(funcionamento, '')::timestamp AS funcionamento,
        tipomanutencao,
        prioridade,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (funcionamento - parada)) / 3600.0), 2) AS downtime_medio_h
FROM base
WHERE abertura IS NOT NULL
  AND parada IS NOT NULL
  AND funcionamento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND funcionamento >= parada;
```
- **Validações de consistência sugeridas:** checar OS com parada/funcionamento fora de ordem; comparar média com mediana.

### Mediana Tempo Equipamento Parado
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:386`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** mediana do tempo de parada (horas) para OS críticas.
- **Fórmula:** `MEDIAN(funcionamento - parada)` em horas.
- **Campos/tabelas:** mesmos do indicador “Downtime Médio Crítico”.
- **Filtros:** mesmos do indicador “Downtime Médio Crítico”.
- **Regras de limpeza e tratamento:** remove OS sem `parada`/`funcionamento`; remove tempos negativos; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:590-658.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:386.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(parada, '')::timestamp AS parada,
        NULLIF(funcionamento, '')::timestamp AS funcionamento,
        tipomanutencao,
        prioridade,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (funcionamento - parada)) / 3600.0)
, 2) AS mediana_h
FROM base
WHERE abertura IS NOT NULL
  AND parada IS NOT NULL
  AND funcionamento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND funcionamento >= parada;
```
- **Validações de consistência sugeridas:** comparar com média; verificar distribuição por equipamento.

### Taxa de Disponibilidade
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:419`.
- **Fonte de dados:** tabelas `consulta_equipamentos` (inventário) e `consulta_os` (downtime).
- **Definição (negócio):** percentual de disponibilidade do parque no período.
- **Fórmula:** `(horas_potenciais - horas_parado) / horas_potenciais * 100`, onde `horas_potenciais = 24 * dias_periodo * qtd_equipamentos`.
- **Campos/tabelas:** `consulta_equipamentos.tag`; `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`.
- **Filtros:** período por `abertura` nas OS; `tipomanutencao = 'CORRETIVA'`; empresa opcional; dias calculados por `data_inicio`/`data_fim` (fallback 30 dias).
- **Regras de limpeza e tratamento:** tags vazias removidas; deduplicação de OS por (`os`,`tag`,`local_api`); tempos negativos removidos.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:659-747.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-448.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:419.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH inventario AS (
    SELECT COUNT(DISTINCT tag) AS qtd_equip
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL
      AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
),
os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
),
downtime AS (
    SELECT SUM(EXTRACT(EPOCH FROM (fechamento - abertura)) / 3600.0) AS horas_parado
    FROM os_base
    WHERE abertura IS NOT NULL
      AND fechamento IS NOT NULL
      AND abertura >= :data_inicio::timestamp
      AND abertura <= (:data_fim::timestamp + interval '23:59:59')
      AND UPPER(tipomanutencao) = 'CORRETIVA'
      AND fechamento >= abertura
)
SELECT ROUND(
    ( (24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * inventario.qtd_equip)
      - COALESCE(downtime.horas_parado, 0) )
    / NULLIF(24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * inventario.qtd_equip, 0)
    * 100
, 2) AS taxa_disponibilidade
FROM inventario, downtime;
```
- **Validações de consistência sugeridas:** cruzar com disponibilidade por unidade (gráficos); validar inventário vs cadastro; checar OS sem fechamento.

⚠️ Divergência detectada: o KPI “Taxa de Disponibilidade” (indicadores) usa inventário de `consulta_equipamentos` e downtime por OS corretivas; o gráfico “Taxa de Disponibilidade Geral dos Equipamentos” usa inventário derivado de `consulta_os` e exige `situacao='Fechada'`, podendo gerar percentuais diferentes para o mesmo período.

### Disp. Equip. Críticos
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:452`.
- **Fonte de dados:** tabelas `consulta_os` e `consulta_equipamentos`.
- **Definição (negócio):** disponibilidade de equipamentos críticos (prioridade ALTA) no período.
- **Fórmula:** `(horas_potenciais_criticos - horas_parado_criticos) / horas_potenciais_criticos * 100`.
- **Campos/tabelas:** `consulta_os.prioridade`, `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`, `consulta_equipamentos.tag`.
- **Filtros:** período por `abertura`; apenas tags com `prioridade` contendo “ALTA”; `tipomanutencao = 'CORRETIVA'`.
- **Regras de limpeza e tratamento:** tags críticas derivadas do df_os; deduplicação por (`os`,`tag`,`local_api`); tempos negativos removidos.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:748-842.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-448.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:452.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH tags_criticas AS (
    SELECT DISTINCT tag
    FROM consulta_os
    WHERE UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND tag IS NOT NULL
      AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
),
inventario AS (
    SELECT COUNT(DISTINCT e.tag) AS qtd_criticos
    FROM consulta_equipamentos e
    JOIN tags_criticas t ON t.tag = e.tag
    WHERE (:empresa IS NULL OR e.empresa = :empresa)
),
os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        tag,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
),
downtime AS (
    SELECT SUM(EXTRACT(EPOCH FROM (fechamento - abertura)) / 3600.0) AS horas_parado
    FROM os_base
    WHERE abertura IS NOT NULL
      AND fechamento IS NOT NULL
      AND abertura >= :data_inicio::timestamp
      AND abertura <= (:data_fim::timestamp + interval '23:59:59')
      AND UPPER(tipomanutencao) = 'CORRETIVA'
      AND fechamento >= abertura
      AND tag IN (SELECT tag FROM tags_criticas)
)
SELECT ROUND(
    ( (24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * inventario.qtd_criticos)
      - COALESCE(downtime.horas_parado, 0) )
    / NULLIF(24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * inventario.qtd_criticos, 0)
    * 100
, 2) AS taxa_disponibilidade_criticos
FROM inventario, downtime;
```
- **Validações de consistência sugeridas:** comparar com o gráfico de disponibilidade crítica; validar definição de “crítico” (ALTA); checar tags críticas sem cadastro.

⚠️ Divergência detectada: o KPI de críticos usa tags críticas apenas do recorte carregado em `df_os`; o gráfico de disponibilidade crítica usa histórico de OS com prioridade ALTA (inventário crítico derivado de `consulta_os`).

### Equipamentos Indisponíveis
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:485`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** quantidade de equipamentos únicos que tiveram parada registrada no período.
- **Fórmula:** `COUNT(DISTINCT tag)` de OS com `parada` preenchida.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.parada`, `consulta_os.tag`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove OS sem `parada`; deduplicação por `tag`.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:843-891.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:485.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT COUNT(DISTINCT tag) AS equip_indisponiveis
FROM consulta_os
WHERE tag IS NOT NULL
  AND tag <> ''
  AND NULLIF(parada, '') IS NOT NULL
  AND NULLIF(abertura, '')::timestamp >= :data_inicio::timestamp
  AND NULLIF(abertura, '')::timestamp <= (:data_fim::timestamp + interval '23:59:59')
  AND (:empresa IS NULL OR empresa = :empresa);
```
- **Validações de consistência sugeridas:** cruzar com lista de OS com `parada`; checar equipamentos repetidos no período.

### Críticos Indisponíveis
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:524`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** quantidade de equipamentos críticos (prioridade ALTA) com parada registrada no período.
- **Fórmula:** `COUNT(DISTINCT tag)` onde `parada` preenchida e `prioridade` contém “ALTA”.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.parada`, `consulta_os.prioridade`, `consulta_os.tag`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `prioridade` contém “ALTA”.
- **Regras de limpeza e tratamento:** remove OS sem `parada`; deduplicação por `tag`.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:892-940.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:524.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT COUNT(DISTINCT tag) AS criticos_indisponiveis
FROM consulta_os
WHERE tag IS NOT NULL
  AND tag <> ''
  AND NULLIF(parada, '') IS NOT NULL
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND NULLIF(abertura, '')::timestamp >= :data_inicio::timestamp
  AND NULLIF(abertura, '')::timestamp <= (:data_fim::timestamp + interval '23:59:59')
  AND (:empresa IS NULL OR empresa = :empresa);
```
- **Validações de consistência sugeridas:** checar se a prioridade “ALTA” está padronizada; cruzar com OS críticas abertas no período.

### % Resolução no Período
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:563`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** percentual de OS corretivas abertas no período que também foram fechadas até `data_fim`.
- **Fórmula:** `(OS abertas e fechadas até o fim) / (OS abertas no período) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.tipomanutencao`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`); considera fechadas apenas com `fechamento` não nulo e <= `data_fim`.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:941-1009.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:563.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    100.0 * SUM(CASE WHEN fechamento IS NOT NULL
                      AND fechamento <= (:data_fim::timestamp + interval '23:59:59') THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0)
, 2) AS taxa_resolucao
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA';
```
- **Validações de consistência sugeridas:** comparar com total de corretivas fechadas dentro do mês; checar OS abertas no período mas fechadas fora.

### Pendências / Equip.
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:596`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** média de OS corretivas abertas/pendentes por equipamento.
- **Fórmula:** `(Qtd OS abertas ou pendentes) / (Qtd tags distintas)`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.situacao`, `consulta_os.tipomanutencao`, `consulta_os.tag`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; `situacao IN ('ABERTA','PENDENTE')`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1010-1071.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:596.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        situacao,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT tag), 0), 2) AS pendencias_por_equip
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(situacao, '')) IN ('ABERTA', 'PENDENTE');
```
- **Validações de consistência sugeridas:** conferir se tags com múltiplas OS no período são contadas corretamente; checar consistência de status.

### Cumprimento Preventiva
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:635`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** percentual de OS preventivas abertas no período que estão fechadas.
- **Fórmula:** `(Preventivas fechadas / Preventivas abertas) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.tipomanutencao`, `consulta_os.situacao`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'PREVENTIVA'`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1072-1129.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:635.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        situacao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    100.0 * SUM(CASE WHEN LOWER(COALESCE(situacao, '')) = 'fechada' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0)
, 2) AS cumprimento_preventiva
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'PREVENTIVA';
```
- **Validações de consistência sugeridas:** comparar com gráfico de taxa de cumprimento por unidade; checar status “Fechada”.

### Cumprimento Calibração
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:668`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** percentual de OS de calibração abertas no período que estão fechadas.
- **Fórmula:** `(Calibrações fechadas / Calibrações abertas) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.tipomanutencao`, `consulta_os.situacao`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CALIBRAÇÃO'`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1130-1187.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:668.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        situacao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    100.0 * SUM(CASE WHEN LOWER(COALESCE(situacao, '')) = 'fechada' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0)
, 2) AS cumprimento_calibracao
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CALIBRAÇÃO';
```
- **Validações de consistência sugeridas:** validar grafia de “CALIBRAÇÃO”; comparar com taxa de cumprimento por unidade.

### Cumprimento Treinamento
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:701`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** percentual de OS de treinamento abertas no período que estão fechadas.
- **Fórmula:** `(Treinamentos fechados / Treinamentos abertos) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.tipomanutencao`, `consulta_os.situacao`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'TREINAMENTO'`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1188-1245.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:701.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        situacao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    100.0 * SUM(CASE WHEN LOWER(COALESCE(situacao, '')) = 'fechada' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0)
, 2) AS cumprimento_treinamento
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'TREINAMENTO';
```
- **Validações de consistência sugeridas:** checar se a tipomanutencao está padronizada; comparar com taxa de cumprimento por unidade.

### Cumprimento TSE
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), card em `eng_clinica/templates/engenharia/indicadores.html:734`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** percentual de OS de TSE abertas no período que estão fechadas.
- **Fórmula:** `(TSE fechadas / TSE abertas) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.tipomanutencao`, `consulta_os.situacao`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'TESTE DE SEGURANÇA ELÉTRICA - TSE'`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1246-1303.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:734.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        situacao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT ROUND(
    100.0 * SUM(CASE WHEN LOWER(COALESCE(situacao, '')) = 'fechada' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(*), 0)
, 2) AS cumprimento_tse
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'TESTE DE SEGURANÇA ELÉTRICA - TSE';
```
- **Validações de consistência sugeridas:** validar se o tipo de manutenção está padronizado; comparar com taxa de cumprimento por unidade.

⚠️ Divergência detectada: os KPIs de cumprimento em indicadores são separados por tipo e usam “TESTE DE SEGURANÇA ELÉTRICA - TSE”; o gráfico de “taxa de cumprimento” agrega tipos diferentes (PREVENTIVA/CALIBRAÇÃO/QUALIFICAÇÃO/TSE) e usa o literal “TSE”, sem incluir TREINAMENTO.

### Maiores Causas de Corretivas
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), tabela em `eng_clinica/templates/engenharia/indicadores.html:767-804`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** top 10 causas de OS corretivas (exceto abertas/pendentes) no período.
- **Fórmula:** `COUNT(*)` por causa + cálculo de percentual sobre o total.
- **Campos/tabelas:** `consulta_os.causa`, `consulta_os.tipomanutencao`, `consulta_os.situacao`, `consulta_os.abertura`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; `situacao NOT IN ('ABERTA','PENDENTE')`.
- **Regras de limpeza e tratamento:** causa nula/vazia vira “NÃO INFORMADO”; deduplicação por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:93-156.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-430.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:767-804.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        situacao,
        COALESCE(NULLIF(causa, ''), 'NÃO INFORMADO') AS causa,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
),
contagem AS (
    SELECT causa, COUNT(*) AS qtd
    FROM base
    WHERE abertura IS NOT NULL
      AND abertura >= :data_inicio::timestamp
      AND abertura <= (:data_fim::timestamp + interval '23:59:59')
      AND UPPER(tipomanutencao) = 'CORRETIVA'
      AND UPPER(COALESCE(situacao, '')) NOT IN ('ABERTA', 'PENDENTE')
    GROUP BY causa
)
SELECT causa,
       qtd,
       ROUND(100.0 * qtd / NULLIF(SUM(qtd) OVER (), 0), 1) AS percent
FROM contagem
ORDER BY qtd DESC
LIMIT 10;
```
- **Validações de consistência sugeridas:** comparar com o gráfico de causas corretivas; checar distribuição de “NÃO INFORMADO”.

⚠️ Divergência detectada: o indicador exclui OS com `situacao` ABERTA/PENDENTE; o gráfico “Principais Causas de Corretivas” não aplica esse filtro e pode contar causas diferentes.

### OS Corretivas por Família
- **Onde aparece:** rota `/eng_clinica/indicadores/` (eng_clinica/urls.py:7-8), tabela em `eng_clinica/templates/engenharia/indicadores.html:820-854`.
- **Fonte de dados:** tabelas `consulta_os` e `consulta_equipamentos`.
- **Definição (negócio):** top 20 famílias com maior número de OS corretivas abertas nos últimos 3 anos.
- **Fórmula:** `COUNT(*)` de OS corretivas por família.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.tipomanutencao`, `consulta_os.tag`; `consulta_equipamentos.tag`, `consulta_equipamentos.familia`.
- **Filtros:** OS com `abertura >= (hoje - 3 anos)`; `tipomanutencao = 'CORRETIVA'`.
- **Regras de limpeza e tratamento:** deduplicação por (`os`,`tag`,`local_api`); remoção de famílias vazias; deduplicação de tags no cadastro.
- **Trechos do código (Backend - cálculo):** eng_clinica/services/indicadores/indicadores_dashboards.py:1358-1419.
- **Trechos do código (Backend - query):** eng_clinica/views.py:414-448.
- **Trechos do código (Frontend):** eng_clinica/templates/engenharia/indicadores.html:820-854.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim (não aplicados ao cálculo no código)
WITH os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
),
filtradas AS (
    SELECT *
    FROM os_base
    WHERE abertura >= (CURRENT_DATE - INTERVAL '3 years')
      AND UPPER(tipomanutencao) = 'CORRETIVA'
),
familias AS (
    SELECT DISTINCT ON (tag)
        tag,
        familia
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL
      AND tag <> ''
)
SELECT f.familia,
       COUNT(*) AS qtd_corretivas
FROM filtradas o
JOIN familias f ON f.tag = o.tag
WHERE f.familia IS NOT NULL
  AND f.familia <> ''
GROUP BY f.familia
ORDER BY qtd_corretivas DESC
LIMIT 20;
```
- **Validações de consistência sugeridas:** validar se o período “últimos 3 anos” é o desejado; verificar famílias nulas; comparar com contagem total de corretivas no período.

⚠️ Riscos e hipóteses: a função presume que os equipamentos já foram filtrados por data de cadastro, mas a view não aplica esse filtro antes de chamar o KPI; a janela temporal ignora `data_inicio`/`data_fim`.

## Gráficos
### Tempo médio de atendimento por unidade (h)
- **Onde aparece:** rota `/eng_clinica/graficos/` (eng_clinica/urls.py:7), card em `eng_clinica/templates/engenharia/graficos.html:40` com `<canvas id="chartAtendimentoMedio">` em `eng_clinica/templates/engenharia/graficos.html:43`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** média do tempo entre abertura e primeiro atendimento por unidade (empresa).
- **Fórmula:** `AVG(data_atendimento - abertura)` em horas, agrupado por empresa.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.data_atendimento`, `consulta_os.empresa`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; empresa opcional.
- **Regras de limpeza e tratamento:** remove datas inválidas; remove tempos negativos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:8-60.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:40-43.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:152-169.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT empresa,
       ROUND(AVG(EXTRACT(EPOCH FROM (data_atendimento_ts - abertura_ts)) / 3600.0), 2) AS tempo_medio_h
FROM (
    SELECT empresa,
           NULLIF(abertura, '')::timestamp AS abertura_ts,
           NULLIF(data_atendimento, '')::timestamp AS data_atendimento_ts
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
) t
WHERE abertura_ts IS NOT NULL
  AND data_atendimento_ts IS NOT NULL
  AND abertura_ts >= :data_inicio::timestamp
  AND abertura_ts <= (:data_fim::timestamp + interval '23:59:59')
  AND data_atendimento_ts >= abertura_ts
GROUP BY empresa
ORDER BY tempo_medio_h DESC;
```
- **Validações de consistência sugeridas:** comparar com KPI de tempo médio de atendimento; checar outliers extremos.

### Tempo de Reparo x Tempo de Atendimento
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:58` com `<canvas id="chartScatterReparo">` em `eng_clinica/templates/engenharia/graficos.html:61`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** dispersão entre tempo de reparo (dias) e tempo de atendimento (horas) por OS fechada.
- **Fórmula:** `x = (fechamento - abertura)` em dias; `y = (data_atendimento - abertura)` em horas.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.data_atendimento`, `consulta_os.empresa`, `consulta_os.equipamento`.
- **Filtros:** `situacao = 'Fechada'`; `abertura` entre `data_inicio` e `data_fim`; empresa opcional.
- **Regras de limpeza e tratamento:** remove datas inválidas; remove tempos negativos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:61-118.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:58-61.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:176-206.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT empresa,
       equipamento AS familia,
       EXTRACT(EPOCH FROM (fechamento_ts - abertura_ts)) / 86400.0 AS x_dias,
       EXTRACT(EPOCH FROM (data_atendimento_ts - abertura_ts)) / 3600.0 AS y_horas
FROM (
    SELECT empresa,
           equipamento,
           NULLIF(abertura, '')::timestamp AS abertura_ts,
           NULLIF(fechamento, '')::timestamp AS fechamento_ts,
           NULLIF(data_atendimento, '')::timestamp AS data_atendimento_ts,
           situacao
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
) t
WHERE abertura_ts IS NOT NULL
  AND fechamento_ts IS NOT NULL
  AND data_atendimento_ts IS NOT NULL
  AND LOWER(situacao) = 'fechada'
  AND abertura_ts >= :data_inicio::timestamp
  AND abertura_ts <= (:data_fim::timestamp + interval '23:59:59')
  AND fechamento_ts >= abertura_ts
  AND data_atendimento_ts >= abertura_ts
ORDER BY x_dias ASC;
```
- **Validações de consistência sugeridas:** checar dispersão com tempos negativos; verificar se `equipamento` representa família.

### Tempo médio de reparo por unidade (dia)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:76` com `<canvas id="chartReparoMedio">` em `eng_clinica/templates/engenharia/graficos.html:79`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** média do tempo de reparo (dias) por unidade.
- **Fórmula:** `AVG(fechamento - abertura)` em dias, por empresa.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.empresa`.
- **Filtros:** `situacao = 'Fechada'`; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove datas inválidas; remove tempos negativos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:119-168.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:76-79.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:212-230.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT empresa,
       ROUND(AVG(EXTRACT(EPOCH FROM (fechamento_ts - abertura_ts)) / 86400.0), 2) AS tempo_medio_dias
FROM (
    SELECT empresa,
           NULLIF(abertura, '')::timestamp AS abertura_ts,
           NULLIF(fechamento, '')::timestamp AS fechamento_ts,
           situacao
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
) t
WHERE abertura_ts IS NOT NULL
  AND fechamento_ts IS NOT NULL
  AND LOWER(situacao) = 'fechada'
  AND abertura_ts >= :data_inicio::timestamp
  AND abertura_ts <= (:data_fim::timestamp + interval '23:59:59')
  AND fechamento_ts >= abertura_ts
GROUP BY empresa
ORDER BY tempo_medio_dias DESC;
```
- **Validações de consistência sugeridas:** comparar com MTTR do período; checar OS com fechamento anterior à abertura.

### Quantidade de OS por Tipo de Manutenção
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:96` com `<canvas id="chartOsPorTipoManutencao">` em `eng_clinica/templates/engenharia/graficos.html:99`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** contagem de OS por tipo de manutenção no período.
- **Fórmula:** `COUNT(*)` por `tipomanutencao` com deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.os`, `consulta_os.tag`, `consulta_os.local_api`, `consulta_os.tipomanutencao`, `consulta_os.abertura`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; empresa opcional.
- **Regras de limpeza e tratamento:** remove datas inválidas; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:222-260.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:96-99.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:274-291.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        tipomanutencao,
        NULLIF(abertura, '')::timestamp AS abertura,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT tipomanutencao,
       COUNT(*) AS qtd
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
GROUP BY tipomanutencao
ORDER BY qtd DESC;
```
- **Validações de consistência sugeridas:** conferir se as duplicidades por OS estão controladas; validar tipos fora do dicionário esperado.

### Taxa de cumprimento de prev, calib, quali e TSE (%)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:116` com `<canvas id="chartCumprimentoPrev">` em `eng_clinica/templates/engenharia/graficos.html:119`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** taxa de conclusão de OS para tipos PREVENTIVA, CALIBRAÇÃO, QUALIFICAÇÃO e TSE, por unidade.
- **Fórmula:** `SUM(is_fechada) / COUNT(*) * 100`.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.situacao`, `consulta_os.tipomanutencao`, `consulta_os.empresa`.
- **Filtros:** `abertura` entre `data_inicio` e `data_fim`; `tipomanutencao` em {PREVENTIVA, CALIBRAÇÃO, QUALIFICAÇÃO, TSE}.
- **Regras de limpeza e tratamento:** remove datas inválidas; converte `situacao` em flag fechada.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:169-221.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:116-119.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:236-268.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT empresa,
           NULLIF(abertura, '')::timestamp AS abertura,
           tipomanutencao,
           LOWER(COALESCE(situacao, '')) = 'fechada' AS is_fechada
    FROM consulta_os
    WHERE tipomanutencao IN ('PREVENTIVA', 'CALIBRAÇÃO', 'QUALIFICAÇÃO', 'TSE')
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa,
       ROUND(100.0 * SUM(CASE WHEN is_fechada THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS taxa
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
GROUP BY empresa
ORDER BY taxa DESC;
```
- **Validações de consistência sugeridas:** comparar com KPIs de cumprimento individuais; checar tipos fora do conjunto.

### Quantidade de OS planejadas já realizadas
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:136` com `<canvas id="chartQtdeOSPlanejdasRealizadas">` em `eng_clinica/templates/engenharia/graficos.html:139`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** contagem de OS de causa PLANEJAMENTO que foram fechadas no período.
- **Fórmula:** `COUNT(*)` por empresa, com deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.causa`, `consulta_os.situacao`, `consulta_os.fechamento`, `consulta_os.empresa`.
- **Filtros:** `causa = 'PLANEJAMENTO'`; `situacao = 'Fechada'`; `fechamento` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove fechamentos inválidos; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:261-303.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:136-139.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:297-305.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        empresa,
        NULLIF(fechamento, '')::timestamp AS fechamento
    FROM consulta_os
    WHERE UPPER(COALESCE(causa, '')) = 'PLANEJAMENTO'
      AND LOWER(COALESCE(situacao, '')) = 'fechada'
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa, COUNT(*) AS qtd
FROM base
WHERE fechamento IS NOT NULL
  AND fechamento >= :data_inicio::timestamp
  AND fechamento <= (:data_fim::timestamp + interval '23:59:59')
GROUP BY empresa
ORDER BY qtd DESC;
```
- **Validações de consistência sugeridas:** comparar com total de OS planejadas do período; verificar fechamentos sem causa.

### Quantidade de OS planejadas não fechadas
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:154` com `<canvas id="chartQtdeOSPlanejdasNFechadas">` em `eng_clinica/templates/engenharia/graficos.html:157`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** contagem de OS de causa PLANEJAMENTO que não foram fechadas (exclui canceladas).
- **Fórmula:** `COUNT(*)` por empresa, com deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.causa`, `consulta_os.situacao`, `consulta_os.abertura`, `consulta_os.empresa`.
- **Filtros:** `causa = 'PLANEJAMENTO'`; `situacao NOT IN ('Fechada','Cancelada')`; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove aberturas inválidas; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:304-345.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:154-157.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:311-319.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        empresa,
        NULLIF(abertura, '')::timestamp AS abertura,
        situacao
    FROM consulta_os
    WHERE UPPER(COALESCE(causa, '')) = 'PLANEJAMENTO'
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa, COUNT(*) AS qtd
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND LOWER(COALESCE(situacao, '')) NOT IN ('fechada', 'cancelada')
GROUP BY empresa
ORDER BY qtd DESC;
```
- **Validações de consistência sugeridas:** checar se canceladas estão sendo excluídas; comparar com planejadas fechadas.

### Porcentagem de OS Planejadas Concluídas
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:172` com `<canvas id="chartPorcentagemOSPlanejadasConcluidas">` em `eng_clinica/templates/engenharia/graficos.html:175`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** taxa de conclusão das OS de planejamento.
- **Fórmula:** `SUM(is_fechada) / COUNT(*) * 100`.
- **Campos/tabelas:** `consulta_os.causa`, `consulta_os.situacao`, `consulta_os.fechamento`, `consulta_os.abertura`.
- **Filtros:** `causa = 'Planejamento'`; `situacao <> 'Cancelada'`; período aplicado em `fechamento`.
- **Regras de limpeza e tratamento:** remove fechamentos nulos antes do cálculo; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:346-415.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:172-175.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:325-336.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        empresa,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        situacao
    FROM consulta_os
    WHERE UPPER(COALESCE(causa, '')) = 'PLANEJAMENTO'
      AND LOWER(COALESCE(situacao, '')) <> 'cancelada'
      AND (:empresa IS NULL OR empresa = :empresa)
),
filtradas AS (
    SELECT *
    FROM base
    WHERE fechamento IS NOT NULL
      AND fechamento >= :data_inicio::timestamp
      AND fechamento <= (:data_fim::timestamp + interval '23:59:59')
)
SELECT empresa,
       ROUND(100.0 * SUM(CASE WHEN LOWER(COALESCE(situacao, '')) = 'fechada' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS taxa
FROM filtradas
GROUP BY empresa
ORDER BY taxa DESC;
```
- **Validações de consistência sugeridas:** conferir se o denominador deveria incluir OS não fechadas; comparar com “planejadas não fechadas”.

⚠️ Riscos e hipóteses: o código remove registros sem `fechamento`, o que pode inflar a taxa (denominador reduzido às fechadas).

### Taxa de Disponibilidade Geral dos Equipamentos
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:192` com container `chartTaxaDisponibilidadeEquipamentos` em `eng_clinica/templates/engenharia/graficos.html:195`.
- **Fonte de dados:** tabela `consulta_os` (inventário por tags e downtime).
- **Definição (negócio):** disponibilidade percentual por unidade usando inventário derivado do histórico de OS.
- **Fórmula:** `(horas_potenciais - horas_parado) / horas_potenciais * 100`, por empresa.
- **Campos/tabelas:** `consulta_os.tag`, `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.situacao`.
- **Filtros:** período por `abertura`; apenas OS fechadas; empresa opcional.
- **Regras de limpeza e tratamento:** tags vazias removidas do inventário; remove tempos negativos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:416-512.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:192-195.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:338-371.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH inventario AS (
    SELECT empresa, COUNT(DISTINCT tag) AS qtd_equip
    FROM consulta_os
    WHERE tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
    GROUP BY empresa
),
os_base AS (
    SELECT empresa,
           NULLIF(abertura, '')::timestamp AS abertura,
           NULLIF(fechamento, '')::timestamp AS fechamento
    FROM consulta_os
    WHERE LOWER(COALESCE(situacao, '')) = 'fechada'
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT i.empresa,
       ROUND(
           ( (24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * i.qtd_equip)
             - COALESCE(SUM(EXTRACT(EPOCH FROM (o.fechamento - o.abertura)) / 3600.0), 0) )
           / NULLIF(24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * i.qtd_equip, 0)
           * 100
       , 2) AS taxa
FROM inventario i
LEFT JOIN os_base o ON o.empresa = i.empresa
WHERE o.abertura >= :data_inicio::timestamp
  AND o.abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND o.fechamento IS NOT NULL
  AND o.abertura IS NOT NULL
  AND o.fechamento >= o.abertura
GROUP BY i.empresa, i.qtd_equip
ORDER BY taxa DESC;
```
- **Validações de consistência sugeridas:** comparar com KPI de disponibilidade; checar inventário vs cadastro.

### Taxa de Disponibilidade dos Equipamentos Críticos
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:210` com container `rowDisponibilidadeEquipamentosCriticos` em `eng_clinica/templates/engenharia/graficos.html:214`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** disponibilidade percentual de equipamentos críticos (prioridade ALTA) por unidade.
- **Fórmula:** `(horas_potenciais_criticos - horas_parado_criticos) / horas_potenciais_criticos * 100`.
- **Campos/tabelas:** `consulta_os.tag`, `consulta_os.prioridade`, `consulta_os.abertura`, `consulta_os.fechamento`.
- **Filtros:** prioridade contém “ALTA”; OS fechadas; período por `abertura`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`); remove tempos negativos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:1061-1163.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:210-214.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:375-402.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH inventario AS (
    SELECT empresa, COUNT(DISTINCT tag) AS qtd_criticos
    FROM consulta_os
    WHERE UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
    GROUP BY empresa
),
os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        empresa,
        tag,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento
    FROM consulta_os
    WHERE UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND LOWER(COALESCE(situacao, '')) = 'fechada'
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT i.empresa,
       ROUND(
           ( (24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * i.qtd_criticos)
             - COALESCE(SUM(EXTRACT(EPOCH FROM (o.fechamento - o.abertura)) / 3600.0), 0) )
           / NULLIF(24 * (DATE_PART('day', :data_fim::timestamp - :data_inicio::timestamp) + 1) * i.qtd_criticos, 0)
           * 100
       , 2) AS taxa
FROM inventario i
LEFT JOIN os_base o ON o.empresa = i.empresa
WHERE o.abertura >= :data_inicio::timestamp
  AND o.abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND o.fechamento IS NOT NULL
  AND o.abertura IS NOT NULL
  AND o.fechamento >= o.abertura
GROUP BY i.empresa, i.qtd_criticos
ORDER BY taxa DESC;
```
- **Validações de consistência sugeridas:** comparar com KPI de críticos; validar definição de “crítico”.

### Qtde de Equipamentos Cadastrados por Unidade
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:231` com `<canvas id="chartQTDEquipamentosUnidade">` em `eng_clinica/templates/engenharia/graficos.html:235`.
- **Fonte de dados:** tabela `consulta_equipamentos`.
- **Definição (negócio):** quantidade de equipamentos cadastrados por unidade no período.
- **Fórmula:** `COUNT(DISTINCT tag)` por empresa.
- **Campos/tabelas:** `consulta_equipamentos.tag`, `consulta_equipamentos.cadastro`, `consulta_equipamentos.empresa`.
- **Filtros:** `cadastro` entre `data_inicio` e `data_fim`; empresa opcional.
- **Regras de limpeza e tratamento:** remove tag nula/vazia; deduplica por `tag`.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:513-557.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:231-235.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:410-418.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
SELECT empresa, COUNT(DISTINCT tag) AS qtd
FROM consulta_equipamentos
WHERE tag IS NOT NULL
  AND tag <> ''
  AND (:empresa IS NULL OR empresa = :empresa)
  AND cadastro >= :data_inicio::timestamp
  AND cadastro <= (:data_fim::timestamp + interval '23:59:59')
GROUP BY empresa
ORDER BY qtd DESC;
```
- **Validações de consistência sugeridas:** comparar com KPI de equipamentos cadastrados; checar duplicidade de tags.

### Qtde de Equipamentos Críticos por Unidade
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:250` com `<canvas id="chartEquipCriticosPorUnidade">` em `eng_clinica/templates/engenharia/graficos.html:254`.
- **Fonte de dados:** tabelas `consulta_os` e `consulta_equipamentos`.
- **Definição (negócio):** quantidade de equipamentos críticos por unidade, filtrados por data de instalação.
- **Fórmula:** `COUNT(DISTINCT tag)` de equipamentos críticos, por empresa.
- **Campos/tabelas:** `consulta_os.prioridade`, `consulta_os.tag`; `consulta_equipamentos.instalacao`, `consulta_equipamentos.empresa`, `consulta_equipamentos.tag`.
- **Filtros:** tags críticas definidas por prioridade “ALTA” na `consulta_os`; `instalacao` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove tags vazias; deduplica por `tag`.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:1164-1220.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:250-254.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:424-432.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH tags_criticas AS (
    SELECT DISTINCT tag
    FROM consulta_os
    WHERE UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT e.empresa,
       COUNT(DISTINCT e.tag) AS qtd
FROM consulta_equipamentos e
JOIN tags_criticas t ON t.tag = e.tag
WHERE e.instalacao IS NOT NULL
  AND e.instalacao >= :data_inicio::timestamp
  AND e.instalacao <= (:data_fim::timestamp + interval '23:59:59')
  AND (:empresa IS NULL OR e.empresa = :empresa)
GROUP BY e.empresa
ORDER BY qtd DESC;
```
- **Validações de consistência sugeridas:** comparar com inventário crítico derivado de OS; checar instalação nula.

⚠️ Riscos e hipóteses: o docstring menciona “garantia vence”, mas o filtro real é por `instalacao`.

### Tempo 1º Atendimento Equip. Crítico (h)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:271` com `<canvas id="chartPrimeiroAtendimentoEquipCritico">` em `eng_clinica/templates/engenharia/graficos.html:274`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** tempo médio de 1º atendimento para OS corretivas críticas.
- **Fórmula:** `AVG(data_atendimento - abertura)` em horas, por empresa.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.data_atendimento`, `consulta_os.parada`, `consulta_os.prioridade`, `consulta_os.tipomanutencao`.
- **Filtros:** `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove duplicatas por (`os`,`tag`,`local_api`); exige `data_atendimento >= abertura`; se `parada` existe, exige `data_atendimento >= parada`.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:1221-1293.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:271-274.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:438-446.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        empresa,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(data_atendimento, '')::timestamp AS data_atendimento,
        NULLIF(parada, '')::timestamp AS parada,
        tipomanutencao,
        prioridade
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa,
       ROUND(AVG(EXTRACT(EPOCH FROM (data_atendimento - abertura)) / 3600.0), 2) AS tempo_medio_h
FROM base
WHERE abertura IS NOT NULL
  AND data_atendimento IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND data_atendimento >= abertura
  AND (parada IS NULL OR data_atendimento >= parada)
GROUP BY empresa
ORDER BY tempo_medio_h DESC;
```
- **Validações de consistência sugeridas:** conferir OS críticas sem `data_atendimento`; checar se `parada` é preenchida.

### Idade Média dos Equipamentos por Unidade (Anos)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:291` com `<canvas id="chartIdadeMediaEquipamentosUnidade">` em `eng_clinica/templates/engenharia/graficos.html:294`.
- **Fonte de dados:** tabela `consulta_equipamentos`.
- **Definição (negócio):** idade média do parque por unidade, em anos.
- **Fórmula:** `AVG((hoje - COALESCE(instalacao, cadastro)) / 365.25)`.
- **Campos/tabelas:** `consulta_equipamentos.instalacao`, `consulta_equipamentos.cadastro`, `consulta_equipamentos.tag`, `consulta_equipamentos.empresa`.
- **Filtros:** não aplica `data_inicio`/`data_fim` (comentado no código); empresa opcional.
- **Regras de limpeza e tratamento:** remove equipamentos sem data; deduplica por `tag`; remove idades negativas ou > 100 anos.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:558-620.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:291-294.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:452-460.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim (não aplicados ao cálculo no código)
WITH base AS (
    SELECT DISTINCT ON (tag)
        empresa,
        tag,
        COALESCE(instalacao, cadastro) AS data_ref
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa,
       ROUND(AVG(EXTRACT(EPOCH FROM (NOW() - data_ref)) / (365.25 * 86400)), 1) AS idade_media_anos
FROM base
WHERE data_ref IS NOT NULL
  AND EXTRACT(EPOCH FROM (NOW() - data_ref)) >= 0
GROUP BY empresa
ORDER BY idade_media_anos DESC;
```
- **Validações de consistência sugeridas:** validar idades negativas; checar equipamentos sem `instalacao`/`cadastro`.

⚠️ Riscos e hipóteses: o gráfico ignora os filtros de período do dashboard (código comentado).

### Idade dos Equipamentos por Família (Anos) - Top 20
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:309` com `<canvas id="chartIdadeFamiliaEquipamentos">` em `eng_clinica/templates/engenharia/graficos.html:312`.
- **Fonte de dados:** tabela `consulta_equipamentos`.
- **Definição (negócio):** idade média por família (top 20), em anos.
- **Fórmula:** `AVG((hoje - COALESCE(instalacao, cadastro)) / 365.25)` por família.
- **Campos/tabelas:** `consulta_equipamentos.familia`, `consulta_equipamentos.instalacao`, `consulta_equipamentos.cadastro`, `consulta_equipamentos.tag`.
- **Filtros:** não aplica `data_inicio`/`data_fim` (comentado no código); empresa opcional.
- **Regras de limpeza e tratamento:** remove sem data ou sem família; deduplica por `tag`; remove idades negativas/absurdas; limita top 20.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:621-681.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:309-312.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:466-474.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim (não aplicados ao cálculo no código)
WITH base AS (
    SELECT DISTINCT ON (tag)
        tag,
        familia,
        COALESCE(instalacao, cadastro) AS data_ref
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
)
SELECT familia,
       ROUND(AVG(EXTRACT(EPOCH FROM (NOW() - data_ref)) / (365.25 * 86400)), 1) AS idade_media_anos
FROM base
WHERE data_ref IS NOT NULL
  AND familia IS NOT NULL
  AND familia <> ''
  AND EXTRACT(EPOCH FROM (NOW() - data_ref)) >= 0
GROUP BY familia
ORDER BY idade_media_anos DESC
LIMIT 20;
```
- **Validações de consistência sugeridas:** checar famílias com nomes vazios; comparar com distribuição de idades por unidade.

⚠️ Riscos e hipóteses: o gráfico ignora `data_inicio`/`data_fim` do filtro.

### Maiores tempos de reparo de equipamentos críticos por família (h)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:330` com `<canvas id="chartReparoCritico">` em `eng_clinica/templates/engenharia/graficos.html:335`.
- **Fonte de dados:** tabelas `consulta_os` e `consulta_equipamentos`.
- **Definição (negócio):** média do tempo de reparo (horas) para OS corretivas críticas, agrupado por família (top 20).
- **Fórmula:** `AVG(fechamento - abertura)` em horas por família.
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.fechamento`, `consulta_os.prioridade`, `consulta_os.tipomanutencao`, `consulta_equipamentos.familia`.
- **Filtros:** `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”; `situacao = 'Fechada'`; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** deduplica por (`os`,`tag`,`local_api`); remove tempos negativos; deduplica por `tag` no cadastro; top 20.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:682-760.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:330-335.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:483-491.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        empresa
    FROM consulta_os
    WHERE UPPER(tipomanutencao) = 'CORRETIVA'
      AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND LOWER(COALESCE(situacao, '')) = 'fechada'
      AND (:empresa IS NULL OR empresa = :empresa)
),
familias AS (
    SELECT DISTINCT ON (tag) tag, familia
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL AND tag <> ''
)
SELECT f.familia,
       ROUND(AVG(EXTRACT(EPOCH FROM (o.fechamento - o.abertura)) / 3600.0), 1) AS horas_reparo
FROM os_base o
JOIN familias f ON f.tag = o.tag
WHERE o.abertura IS NOT NULL
  AND o.fechamento IS NOT NULL
  AND o.abertura >= :data_inicio::timestamp
  AND o.abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND o.fechamento >= o.abertura
GROUP BY f.familia
ORDER BY horas_reparo DESC
LIMIT 20;
```
- **Validações de consistência sugeridas:** conferir famílias sem cadastro; comparar com tempos de reparo por unidade.

### Principais Causas de Corretivas
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:353` com `<canvas id="chartCausasCorretivas">` em `eng_clinica/templates/engenharia/graficos.html:357`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** top 10 causas de manutenção corretiva no período.
- **Fórmula:** `COUNT(*)` por causa com deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.causa`, `consulta_os.tipomanutencao`, `consulta_os.abertura`.
- **Filtros:** `tipomanutencao = 'CORRETIVA'`; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove causas nulas/vazias; deduplica por (`os`,`tag`,`local_api`); top 10.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:761-811.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:353-357.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:497-505.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        causa,
        tipomanutencao,
        empresa
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT causa, COUNT(*) AS qtd
FROM base
WHERE abertura IS NOT NULL
  AND abertura >= :data_inicio::timestamp
  AND abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND causa IS NOT NULL
  AND causa <> ''
GROUP BY causa
ORDER BY qtd DESC
LIMIT 10;
```
- **Validações de consistência sugeridas:** comparar com “Maiores Causas de Corretivas” (indicadores); checar % de “NÃO INFORMADO”.

### Maiores tempos de PARADA de equipamentos críticos por família (h)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:375` com `<canvas id="elchartParadaCritica">` em `eng_clinica/templates/engenharia/graficos.html:380`.
- **Fonte de dados:** tabelas `consulta_os` e `consulta_equipamentos`.
- **Definição (negócio):** média do tempo de parada (horas) para OS críticas, por família (top 20).
- **Fórmula:** `AVG(funcionamento - parada)` em horas.
- **Campos/tabelas:** `consulta_os.parada`, `consulta_os.funcionamento`, `consulta_os.prioridade`, `consulta_os.tipomanutencao`, `consulta_equipamentos.familia`.
- **Filtros:** `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove OS sem parada/funcionamento; remove tempos negativos; deduplica por (`os`,`tag`,`local_api`); filtra famílias vazias/#N/A; top 20.
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:812-904.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:375-380.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:511-519.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH os_base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        NULLIF(abertura, '')::timestamp AS abertura,
        NULLIF(parada, '')::timestamp AS parada,
        NULLIF(funcionamento, '')::timestamp AS funcionamento,
        empresa
    FROM consulta_os
    WHERE UPPER(tipomanutencao) = 'CORRETIVA'
      AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND tag IS NOT NULL AND tag <> ''
      AND (:empresa IS NULL OR empresa = :empresa)
),
familias AS (
    SELECT DISTINCT ON (tag) tag, familia
    FROM consulta_equipamentos
    WHERE tag IS NOT NULL AND tag <> ''
)
SELECT f.familia,
       ROUND(AVG(EXTRACT(EPOCH FROM (o.funcionamento - o.parada)) / 3600.0), 1) AS horas_parada
FROM os_base o
JOIN familias f ON f.tag = o.tag
WHERE o.abertura IS NOT NULL
  AND o.parada IS NOT NULL
  AND o.funcionamento IS NOT NULL
  AND o.abertura >= :data_inicio::timestamp
  AND o.abertura <= (:data_fim::timestamp + interval '23:59:59')
  AND o.funcionamento >= o.parada
  AND f.familia IS NOT NULL
  AND f.familia <> ''
  AND f.familia <> '#N/A'
GROUP BY f.familia
ORDER BY horas_parada DESC
LIMIT 20;
```
- **Validações de consistência sugeridas:** comparar com downtime médio crítico; verificar famílias #N/A.

### Tempo MEDIANO de Parada de Críticos por Unidade (h)
- **Onde aparece:** rota `/eng_clinica/graficos/`, card em `eng_clinica/templates/engenharia/graficos.html:395` com `<canvas id="chartMedianaParadaEquipamentosCriticosUnidade">` em `eng_clinica/templates/engenharia/graficos.html:398`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** mediana do tempo de parada (horas) por unidade para OS críticas.
- **Fórmula:** `MEDIAN(funcionamento - parada)` em horas por empresa.
- **Campos/tabelas:** `consulta_os.parada`, `consulta_os.funcionamento`, `consulta_os.fechamento`, `consulta_os.prioridade`, `consulta_os.tipomanutencao`.
- **Filtros:** `fechamento` entre `data_inicio` e `data_fim`; `tipomanutencao = 'CORRETIVA'`; `prioridade` contém “ALTA”.
- **Regras de limpeza e tratamento:** remove OS sem parada/funcionamento/fechamento; remove tempos negativos; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:905-968.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:395-398.
- **Trechos do código (Frontend - Chart.js):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:525-533.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        os,
        tag,
        local_api,
        empresa,
        NULLIF(parada, '')::timestamp AS parada,
        NULLIF(funcionamento, '')::timestamp AS funcionamento,
        NULLIF(fechamento, '')::timestamp AS fechamento,
        tipomanutencao,
        prioridade
    FROM consulta_os
    WHERE (:empresa IS NULL OR empresa = :empresa)
)
SELECT empresa,
       ROUND(
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (funcionamento - parada)) / 3600.0)
       , 1) AS mediana_h
FROM base
WHERE parada IS NOT NULL
  AND funcionamento IS NOT NULL
  AND fechamento IS NOT NULL
  AND fechamento >= :data_inicio::timestamp
  AND fechamento <= (:data_fim::timestamp + interval '23:59:59')
  AND UPPER(tipomanutencao) = 'CORRETIVA'
  AND UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
  AND funcionamento >= parada
GROUP BY empresa
ORDER BY mediana_h DESC;
```
- **Validações de consistência sugeridas:** comparar com downtime médio crítico por unidade; checar fechamentos fora do período.

### Horários em que equipamentos críticos ficaram indisponíveis
- **Onde aparece:** rota `/eng_clinica/graficos/`, tabela heatmap em `eng_clinica/templates/engenharia/graficos.html:416-421`.
- **Fonte de dados:** tabela `consulta_os`.
- **Definição (negócio):** matriz de contagem de OS críticas por hora do dia e dia da semana.
- **Fórmula:** `COUNT(*)` por (hora, dia_semana), após deduplicação por (`os`,`tag`,`local_api`).
- **Campos/tabelas:** `consulta_os.abertura`, `consulta_os.prioridade`, `consulta_os.empresa`.
- **Filtros:** `prioridade` contém “ALTA”; `abertura` entre `data_inicio` e `data_fim`.
- **Regras de limpeza e tratamento:** remove datas inválidas; deduplica por (`os`,`tag`,`local_api`).
- **Trechos do código (Backend - cálculo e query):** eng_clinica/services/graficos/graficos_dashboards.py:969-1060.
- **Trechos do código (Frontend - template):** eng_clinica/templates/engenharia/graficos.html:416-421.
- **Trechos do código (Frontend - render/heatmap):** eng_clinica/static/engenharia/js/dashboard_graficos_charts.js:538-562.
- **SQL auditorável (Postgres):**
```sql
-- use :data_inicio e :data_fim
WITH base AS (
    SELECT DISTINCT ON (os, tag, local_api)
        NULLIF(abertura, '')::timestamp AS abertura,
        empresa
    FROM consulta_os
    WHERE UPPER(COALESCE(prioridade, '')) LIKE '%ALTA%'
      AND (:empresa IS NULL OR empresa = :empresa)
),
filtradas AS (
    SELECT abertura
    FROM base
    WHERE abertura IS NOT NULL
      AND abertura >= :data_inicio::timestamp
      AND abertura <= (:data_fim::timestamp + interval '23:59:59')
)
SELECT EXTRACT(HOUR FROM abertura) AS hora,
       EXTRACT(ISODOW FROM abertura) AS dia_semana_iso,
       COUNT(*) AS qtd
FROM filtradas
GROUP BY EXTRACT(HOUR FROM abertura), EXTRACT(ISODOW FROM abertura)
ORDER BY hora, dia_semana_iso;
```
- **Validações de consistência sugeridas:** conferir se a matriz usa semana ISO (Seg=1..Dom=7); validar distribuição por hora.
