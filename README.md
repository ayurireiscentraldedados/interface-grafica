# API Segurança Viária CE

API pública para consultar, de forma simples, indicadores de acidentes em rodovias federais no Ceará sem exigir que a pessoa usuária baixe e relacione manualmente bases da PRF, IBGE e Open-Meteo.

> Produto da Trilha A — API pública de dados abertos. A API reutiliza como infraestrutura de dados a camada Gold do projeto preexistente **Ceará Road Safety Data Platform**. O trabalho específico desta ação de extensão é a disponibilização pública, documentação, testes, validação com público externo e evolução desta API.

## Para quem é

O produto foi pensado principalmente para:

- estudantes que precisam trabalhar com dados públicos em disciplinas, pesquisas e projetos;
- pesquisadores e profissionais interessados em mobilidade e segurança viária;
- jornalistas de dados que precisam consultar recortes municipais e rodoviários sem preparar toda a base bruta;
- desenvolvedores que queiram consumir indicadores de segurança viária em outros sistemas.

## Estado atual

- A API está **no ar**: https://api-seguranca-viaria-ce.onrender.com (conferida em 13/10/2026). Qualquer pessoa consulta sem cadastro e sem instalar nada.
- Os dados publicados são o pacote `data-2026-08-v1`: 2024 e 2025 completos, e 2026 parcial, até 31/08/2026.
- A documentação interativa, onde dá para testar cada rota no navegador, fica em `/docs`.
- Rotas no ar hoje: municípios, indicadores de um município, rodovias, trechos críticos e acidentes.
- Cinco rotas de análise já estão prontas no código, mas **ainda não estão na URL pública**: o ranking de municípios por habitante, as circunstâncias dos acidentes fatais, o perfil de cada rodovia, a evolução no tempo e o mapa de calor por dia da semana e horário. Elas aparecem na URL pública depois do próximo deploy. Enquanto isso, dá para testá-las rodando a API no seu computador (veja abaixo).
- Os testes automáticos rodam no GitHub a cada envio de código.
- A API guarda só data e hora, método, caminho, status e tempo de cada consulta. Não guarda nome, e-mail nem IP.

### Endereços

- Endereço público: https://api-seguranca-viaria-ce.onrender.com
- Documentação interativa: https://api-seguranca-viaria-ce.onrender.com/docs
- Status da API: https://api-seguranca-viaria-ce.onrender.com/health
- Monitoramento de disponibilidade: UptimeRobot, com verificação do `/health` a cada 5 minutos
- Repositório da equipe: https://github.com/ayurireiscentraldedados/interface-grafica
- Dados usados pela API (arquivo da release): https://github.com/ayurireiscentraldedados/interface-grafica/releases/download/data-2026-08-v1/ceara_road_safety_api.duckdb
- No seu computador: `http://127.0.0.1:8000`, com a documentação em `http://127.0.0.1:8000/docs`. No Windows, prefira `127.0.0.1` a `localhost`: no PowerShell a resposta chega em 0,06 s, contra mais de 2 s com `localhost`.

## Como usar agora

### Jeito mais rápido: usar a API que já está no ar

Não precisa instalar nada nem criar conta. Escolha o jeito que preferir.

**No navegador.** Abra https://api-seguranca-viaria-ce.onrender.com/docs, clique numa rota, depois em "Try it out" e em "Execute". Também dá para colar o endereço direto na barra do navegador, por exemplo:

```text
https://api-seguranca-viaria-ce.onrender.com/api/v1/rodovias?ano=2025&limit=5
```

**No terminal.**

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios/2304400/indicadores?ano=2025'
```

Isso devolve os números de 2025 de Fortaleza (código IBGE 2304400). Para achar o código de outro município, abra `/api/v1/municipios?ano=2025`, que lista os 184 municípios com nome e código. No PowerShell do Windows, use `curl.exe` no lugar de `curl`.

**Em Python** (precisa de `pip install requests pandas`):

```python
import requests
import pandas as pd

URL = "https://api-seguranca-viaria-ce.onrender.com"

resposta = requests.get(f"{URL}/api/v1/rodovias", params={"ano": 2025, "limit": 5})
resposta.raise_for_status()
rodovias = pd.DataFrame(resposta.json()["data"])
print(rodovias[["highway", "accidents", "deaths", "serious_injuries"]])
```

> No Windows PowerShell 5.1 (o que vem com o Windows), o comando `Invoke-RestMethod` troca os acentos (aparece `AcaraÃº` no lugar de `Acaraú`). Os dados estão certos; o problema é de leitura do PowerShell. Use o navegador, o `curl.exe` ou Python.

### Rodar no seu computador

**1. Preparar o ambiente**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

No Windows (PowerShell), o jeito mais seguro é não ativar o ambiente, porque o PowerShell costuma bloquear o script de ativação. Chame o Python do ambiente direto:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Nos passos seguintes, onde aparecer `python` ou `uvicorn`, use `.venv\Scripts\python.exe` e `.venv\Scripts\python.exe -m uvicorn`.

**2. Baixar o banco de dados pronto**

O banco já tratado (cerca de 3 MB) está publicado na release `data-2026-08-v1` do GitHub. Baixe para a pasta `data/`:

```bash
curl -L -o data/ceara_road_safety_api.duckdb \
  https://github.com/ayurireiscentraldedados/interface-grafica/releases/download/data-2026-08-v1/ceara_road_safety_api.duckdb
```

No PowerShell do Windows, use `curl.exe` no lugar de `curl`.

Quem tem o projeto principal (Ceará Road Safety Data Platform) ao lado deste repositório também pode gerar o banco do zero:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

Ou:

```bash
make export SOURCE_DB=../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

**3. Iniciar a API**

```bash
uvicorn app.main:app --reload --port 8000
```

**4. Testar uma consulta**

```bash
curl 'http://127.0.0.1:8000/api/v1/municipios?ano=2025&limit=2'
```

A resposta é assim:

```json
{
  "count": 2,
  "filters": {"ano": 2025},
  "data": [
    {"ibge_code": "2300101", "municipality": "Abaiara"},
    {"ibge_code": "2300150", "municipality": "Acarape"}
  ]
}
```

**5. Rodar os testes**

```bash
python -m pytest -q
```

Os testes usam um banco temporário criado só para eles, com números inventados. Veja mais na seção "Testes automatizados".

## De onde vêm os dados

| Fonte | Órgão/provedor | Endereço | Atualização / dado usado no projeto |
| :-- | :-- | :-- | :-- |
| Acidentes em rodovias federais | Polícia Rodoviária Federal (PRF) | https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf | PRF declara atualização mensal para a base BAT. O recorte usado pela plataforma contém 2024, 2025 e 2026; 2026 é parcial. |
| Municípios e estimativas populacionais | IBGE | https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html | A estimativa municipal de 2026 tem data de referência de 01/07/2026. |
| Condições meteorológicas históricas | Open-Meteo | https://open-meteo.com/en/docs/historical-weather-api | Dados históricos associados ao horário/local das ocorrências processadas. |

### Procedência e transformação

A API **não consulta as três fontes a cada requisição**. Os dados são preparados antes no Ceará Road Safety Data Platform:

```text
PRF + IBGE + Open-Meteo
        ↓
Bronze → Silver → Gold
        ↓
DuckDB analítico
        ↓
export_gold.py
        ↓
DuckDB compacto da API
        ↓
FastAPI
```

Isso permite que a API publique dados já tratados, relacionados e validados sem acoplar o serviço público ao pipeline completo.

## Licença

### Dados

- **PRF:** a página institucional de Dados Abertos informa que os dados podem ser usados, reutilizados e redistribuídos livremente, dentro da Política de Dados Abertos do Poder Executivo Federal.
- **IBGE:** os dados utilizados são publicados nos canais de dados abertos e estatísticos do IBGE. A fonte deve ser mantida explicitamente atribuída nas reutilizações.
- **Open-Meteo:** os dados obtidos pela API estão sujeitos a **CC BY 4.0** e exigem atribuição. O serviço gratuito é destinado a uso não comercial e possui limites de chamadas publicados pelo provedor.

Consulte sempre os termos das fontes originais antes de redistribuir o produto em outro contexto.

### Código e material desta equipe

O código deste repositório é disponibilizado sob **MIT License**. Veja `LICENSE`.

## O que este produto não faz

- Não representa todos os acidentes de trânsito do Ceará: a base principal da PRF cobre acidentes registrados em **rodovias federais**.
- O ano de 2026 é parcial no recorte atualmente utilizado e não deve ser comparado diretamente com anos completos sem observar a janela de coleta.
- Frequência de acidentes envolvendo um tipo ou modelo de veículo não mede risco relativo sem um denominador de exposição/frota.
- As taxas per capita dependem das estimativas populacionais do IBGE e de sua metodologia; municípios pequenos têm taxas instáveis, pois poucos casos já alteram muito o valor.
- A análise de circunstâncias mostra frequência entre acidentes já registrados, não risco de se acidentar; a "causa" é a causa presumida registrada pela PRF, não uma causa comprovada.
- O perfil por rodovia compara contagens observadas; sem dados de tráfego (veículos por dia, extensão percorrida) não mede risco por viagem nem por km rodado, e rodovias mais longas ou mais movimentadas acumulam mais ocorrências.
- A variação percentual entre períodos mostra mudança na contagem de acidentes registrados, não mudança de risco. Em recortes pequenos (um município, uma rodovia, um mês), poucos casos já mudam muito o percentual. O ano parcial é comparado com o mesmo intervalo do ano anterior, e não com o ano inteiro.
- O mapa de calor por dia da semana e horário mostra onde os acidentes se concentram, não onde é mais perigoso: sem dados de tráfego, não dá para saber se sexta à noite concentra mais acidentes por ter mais gente na estrada.
- Associação entre clima, local, horário ou tipo de veículo e acidentes não implica causalidade.
- Trechos com maior número observado de acidentes são concentrações históricas na base, não previsões de perigo futuro.
- A API é somente leitura e não recebe registros de acidentes da população.
- Os dados podem conter ausências e limitações herdadas das fontes originais.

## Contato

- Contato da equipe — [GitHub Issues](https://github.com/ayurireiscentraldedados/interface-grafica/issues)
- Repositório — https://github.com/ayurireiscentraldedados/interface-grafica

---

# Rotas

A documentação interativa completa é gerada automaticamente pelo FastAPI em `/docs`.

## `GET /`

**O que faz:** apresenta nome, versão e caminhos principais do serviço.

**Exemplo:**

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/'
```

## `GET /health`

**O que faz:** informa se a API está ativa e se o banco analítico está disponível.

**Exemplo:**

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/health'
```

**Possíveis respostas:**

- `status=ok`: banco carregado;
- `status=degraded`: API subiu, mas o banco ainda não foi exportado.

## `GET /api/v1/datasets`

**O que faz:** lista os datasets realmente disponíveis no banco publicado e suas colunas.

**Parâmetros:** nenhum.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/datasets'
```

## `GET /api/v1/municipios`

**O que faz:** lista os municípios disponíveis no recorte analítico.

**Parâmetros:**

- `ano` — opcional;
- `limit` — 1 a 500, padrão 184.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios?ano=2025'
```

**Erros possíveis:**

- `422`: parâmetro inválido;
- `503`: banco/dataset ainda não disponível.

## `GET /api/v1/municipios/{ibge_code}/indicadores`

**O que faz:** devolve os indicadores anuais do município identificado pelo código IBGE.

**Parâmetros:**

- `ibge_code` — obrigatório no caminho; é o código IBGE do município, por exemplo `2304400` (Fortaleza);
- `ano` — opcional.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios/2304400/indicadores?ano=2025'
```

**Erros possíveis:**

- `404`: combinação município/ano não encontrada;
- `422`: ano fora da faixa aceita;
- `503`: banco/dataset indisponível.

## `GET /api/v1/municipios/risco-per-capita`

**O que faz:** rankeia municípios por acidentes, mortes e feridos graves por 100 mil habitantes, usando a população já presente na mart municipal. Evita que municípios grandes apareçam no topo só por terem mais habitantes.

**Parâmetros:**

- `ano` — opcional; quando omitido, linhas de anos diferentes são comparadas juntas;
- `ordenar_por` — opcional: `acidentes` (padrão), `mortes` ou `feridos_graves`;
- `limit` — 1 a 184, padrão 20.

```bash
curl 'http://127.0.0.1:8000/api/v1/municipios/risco-per-capita?ano=2025&ordenar_por=mortes&limit=10'
```

> Ainda não está na URL pública; aparece depois do próximo deploy. Para testar agora, rode a API no seu computador.

Cada item traz `population`, os valores brutos e as taxas `accidents_per_100k`, `deaths_per_100k` e `serious_injuries_per_100k`. Quando a população está ausente ou é zero, as taxas vêm `null` e a linha vai para o fim do ranking.

**Erros possíveis:**

- `422`: `ano`, `limit` ou `ordenar_por` fora dos valores aceitos;
- `503`: banco/dataset indisponível, mart sem coluna de população, ou indicador escolhido ausente nesta exportação.

## `GET /api/v1/analises/circunstancias`

**O que faz:** responde quais circunstâncias registradas aparecem com mais frequência nos acidentes fatais. Agrupa as ocorrências por uma dimensão e informa, para cada categoria, quantos acidentes houve, quantos foram fatais, a taxa de fatalidade dentro da categoria e a fatia da categoria no total de acidentes fatais.

**Parâmetros:**

- `dimensao` — `causa` (padrão, causa presumida registrada), `tipo_acidente`, `condicao_pista` ou `iluminacao`;
- `ano` — opcional;
- `municipio` — opcional;
- `ordenar_por` — `fatais` (padrão, mais acidentes fatais primeiro) ou `taxa_fatal`;
- `min_acidentes` — mínimo de acidentes por categoria, padrão 1; use um valor maior com `ordenar_por=taxa_fatal` para ignorar categorias pequenas;
- `limit` — 1 a 100, padrão 20.

```bash
curl 'http://127.0.0.1:8000/api/v1/analises/circunstancias?dimensao=iluminacao&ano=2025'
```

> Ainda não está na URL pública; aparece depois do próximo deploy. Para testar agora, rode a API no seu computador.

Cada item traz `categoria`, `acidentes`, `acidentes_fatais`, `taxa_fatal_pct` e `pct_dos_acidentes_fatais`. A resposta inclui também `total_acidentes`, `total_acidentes_fatais` e um `aviso` sobre a interpretação. Valores vazios aparecem como `Não informado`. Um acidente é fatal quando há mortes registradas ou, na falta dessa coluna, quando a classificação indica vítimas fatais.

**No banco publicado hoje:** só a dimensão `iluminacao` (fase do dia) está disponível. `causa`, `tipo_acidente` e `condicao_pista` respondem `503`, porque essas colunas não foram incluídas no banco exportado. Para ativá-las, é preciso exportar da plataforma principal a causa, o tipo do acidente e a condição da pista.

**Erros possíveis:**

- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, dimensão sem coluna correspondente na tabela de acidentes publicada, ou tabela sem indicação de gravidade.

## `GET /api/v1/analises/perfil-rodovia`

**O que faz:** monta um perfil comparável de cada rodovia federal e responde quais rodovias têm os perfis mais preocupantes e o que predomina em cada uma. Combina os totais por rodovia (como em `/rodovias`), a distribuição das ocorrências por horário, clima e tipo de veículo, e os trechos mais críticos (como em `/trechos-criticos`). Quando `ano` é omitido, os anos são somados.

**Parâmetros:**

- `rodovia` — opcional; devolve só o perfil dessa rodovia. Aceita `116` ou `BR-116` (no banco publicado as rodovias aparecem só com o número);
- `ano` — opcional;
- `ordenar_por` — `mortes` (padrão), `acidentes` ou `mortes_por_100_acidentes`;
- `min_acidentes` — mínimo de acidentes por rodovia, padrão 1; use um valor maior com `mortes_por_100_acidentes` para ignorar rodovias pequenas;
- `trechos` — quantos trechos críticos listar por rodovia, de 0 a 10, padrão 3;
- `limit` — 1 a 50, padrão 10.

```bash
curl 'http://127.0.0.1:8000/api/v1/analises/perfil-rodovia?ano=2025&ordenar_por=mortes_por_100_acidentes&min_acidentes=50'
```

> Ainda não está na URL pública; aparece depois do próximo deploy. Para testar agora, rode a API no seu computador.

Cada perfil traz `posicao`, `acidentes`, `mortes`, `feridos_graves`, `mortes_por_100_acidentes`, `pct_acidentes_fatais`, `predominantes` (a categoria mais frequente de `horario`, `clima` e `tipo_veiculo`), `distribuicoes` (as 3 categorias mais frequentes, com contagem e percentual) e `trechos_criticos` (`km_inicial`, `km_final`, `acidentes`, `mortes`).

`pct_acidentes_fatais` e `distribuicoes` vêm das ocorrências mapeadas (`ocorrencias_mapeadas`), que podem divergir dos totais da tabela de rodovias. Dimensões ausentes no banco publicado são listadas em `dimensoes_indisponiveis` e omitidas do perfil. No banco publicado hoje, `tipo_veiculo` aparece como indisponível, porque a tabela de ocorrências não traz o tipo de veículo. Também existe uma "rodovia" chamada `0` (14 ocorrências), que parece ser registro sem rodovia identificada; confirme na plataforma antes de citá-la.

**Erros possíveis:**

- `404`: rodovia/ano não encontrada;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível ou tabela de rodovias sem coluna de mortes para a ordenação escolhida.

## `GET /api/v1/analises/evolucao`

**O que faz:** devolve a série de acidentes, mortes e feridos graves por ano ou por mês, com a variação percentual contra o período anterior. Evita chamar a API uma vez por ano e montar a série à mão. Sem filtro, vale o total do Ceará.

**Parâmetros:**

- `granularidade` — `ano` (padrão) ou `mes`;
- `ano` — opcional; só escolhe quais períodos aparecem, as variações continuam calculadas contra o período anterior;
- `municipio` — opcional, pelo nome (sem diferenciar maiúsculas);
- `rodovia` — opcional; aceita `116` ou `BR-116`;
- `comparar` — `mesmo_periodo` (padrão) ou `total`. Só muda o resultado quando o último ano é parcial.

```bash
curl 'http://127.0.0.1:8000/api/v1/analises/evolucao?granularidade=mes&municipio=Fortaleza&ano=2026'
```

> Ainda não está na URL pública; aparece depois do próximo deploy. Para testar agora, rode a API no seu computador.

Cada período traz `periodo`, `acidentes`, `mortes`, `feridos_graves`, `parcial`, `var_pct_acidentes`, `var_pct_mortes`, `var_pct_feridos_graves` e `base_comparacao`, que diz com o quê o período foi comparado. Na série mensal, a variação é contra o mês anterior e vem também `var_pct_mesmo_mes_ano_anterior`, que não sofre com sazonalidade. A variação é `null` quando o período-base é zero ou não existe. Meses sem nenhum acidente aparecem com zero.

**Ano parcial.** A resposta traz `periodo_parcial` (por exemplo, `{"ano": 2026, "ate": "2026-08-31"}`), tirado da data até a qual a base foi observada. Com `comparar=mesmo_periodo`, o ano parcial é comparado com o **mesmo intervalo** do ano anterior (1º de janeiro até 31/08), para 2026 não parecer uma queda de 30% só por ter menos meses. Com `comparar=total`, ele é comparado com o ano anterior inteiro.

**De onde vêm os números.** `fonte` informa: `mart anual` (mesmos totais de `/rodovias` e de `/municipios/{ibge}/indicadores`) ou `ocorrências mapeadas` (série mensal, ou município e rodovia juntos). No banco publicado, os dois dão os mesmos totais anuais; se uma exportação futura divergir, o `aviso` já diz isso. Ocorrências sem data ficam fora da série mensal.

**Erros possíveis:**

- `404`: município, rodovia ou ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, ou série mensal pedida com uma tabela de acidentes sem data da ocorrência.

## `GET /api/v1/analises/quando-acontece`

**O que faz:** mostra quando os acidentes acontecem, cruzando dia da semana com faixa horária, para montar um mapa de calor. Responde perguntas como "sexta à noite é pior?".

**Parâmetros:**

- `ano` — opcional;
- `municipio` — opcional, pelo nome;
- `rodovia` — opcional; aceita `116` ou `BR-116`;
- `faixa` — `turno` (padrão: `madrugada` 0h–5h59, `manhã` 6h–11h59, `tarde` 12h–17h59, `noite` 18h–23h59) ou `hora` (24 faixas, `00h` a `23h`);
- `min_acidentes` — mínimo de acidentes por célula para entrar em `mais_criticos`, padrão 1.

```bash
curl 'http://127.0.0.1:8000/api/v1/analises/quando-acontece?ano=2025&faixa=turno'
```

> Ainda não está na URL pública; aparece depois do próximo deploy. Para testar agora, rode a API no seu computador.

A resposta traz:

- `data`: a grade completa (7 dias × as faixas), **incluindo as células com zero**, sempre na mesma ordem (segunda a domingo, faixas do começo ao fim do dia). Cada célula tem `dia_semana`, `dia_semana_num` (1 = segunda), `faixa`, `acidentes`, `mortes`, `acidentes_fatais`, `taxa_fatal_pct` e `pct_do_total`;
- `por_dia_semana` e `por_faixa`: os totais de cada dia e de cada faixa;
- `mais_criticos`: até 5 células, ordenadas por mortes e depois por acidentes;
- `total_acidentes`, `total_mortes` e `sem_horario` (ocorrências sem data ou hora, que ficam fora das células).

Se a tabela tiver data mas não tiver hora, `faixa` aparece em `dimensoes_indisponiveis`, e a resposta traz só `por_dia_semana`.

**Erros possíveis:**

- `404`: município, rodovia ou ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, ou tabela de acidentes sem data da ocorrência.

## `GET /api/v1/rodovias`

**O que faz:** lista/rankeia rodovias pelos indicadores observados na camada Gold.

**Parâmetros:**

- `ano` — opcional;
- `limit` — 1 a 100, padrão 20.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/rodovias?ano=2025&limit=10'
```

## `GET /api/v1/trechos-criticos`

**O que faz:** lista trechos rodoviários agregados em segmentos de 10 km.

**Parâmetros:**

- `ano` — opcional;
- `rodovia` — opcional; aceita `116` ou `BR-116`;
- `limit` — 1 a 100.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/trechos-criticos?ano=2025&limit=10'
```

## `GET /api/v1/acidentes`

**O que faz:** consulta ocorrências da mart de mapa com paginação simples.

**Parâmetros:**

- `ano` — opcional;
- `municipio` — opcional;
- `limit` — 1 a 500, padrão 100;
- `offset` — início da página, padrão 0.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/acidentes?ano=2025&municipio=Fortaleza&limit=50'
```

## Como rodar localmente com Docker

Primeiro gere `data/ceara_road_safety_api.duckdb`. Depois:

```bash
docker compose up --build -d
```

Confira:

```bash
curl 'http://127.0.0.1:8000/health'
```

Documentação:

```text
http://127.0.0.1:8000/docs
```

Parar:

```bash
docker compose down
```

## Testes automatizados

Os testes usam um DuckDB temporário criado exclusivamente para a suíte; os números da fixture **não são dados reais do projeto**.

```bash
python -m pytest -q
```

ou:

```bash
make test
```

Os testes cobrem os casos que funcionam e também os erros: parâmetro inválido (`422`), município ou rodovia que não existe (`404`), banco ou tabela ausente (`503`) e banco com colunas diferentes do esperado (`500`).

## Evidência de alcance

A API anota, para cada consulta, só isto:

```text
data e hora (UTC), método HTTP, caminho, status e tempo de resposta
```

Ela **não anota nome, e-mail nem IP**, nem os filtros usados na consulta.

**Um cuidado importante com o Render gratuito:** o disco do serviço é apagado toda vez que ele reinicia (por exemplo, a cada novo deploy). Por isso o arquivo `logs/access.csv` da nuvem não serve, sozinho, como registro até o fim do semestre. Para não perder a contagem, cada consulta também é escrita nos logs do Render, em linhas que começam com `ACESSO`.

Para guardar a contagem:

1. De tempos em tempos (por exemplo, toda semana), abra os logs do serviço no painel do Render e copie tudo para um arquivo de texto **fora do repositório**. O Render guarda os logs por pouco tempo, então confira o prazo no painel.
2. Deixe só as linhas de acesso (as que têm `ACESSO`) e salve o resultado em `evidencias/`, com a data no nome. Assim mensagens do servidor que não interessam não vão para o repositório público:

```bash
grep ACESSO logs-do-render.txt > evidencias/2026-11-05-logs-render.txt
```

No PowerShell do Windows:

```powershell
Select-String ACESSO logs-do-render.txt | ForEach-Object { $_.Line } | Set-Content evidencias/2026-11-05-logs-render.txt
```

3. Na hora de contar, passe todos os arquivos juntos. Se dois arquivos tiverem as mesmas linhas, cada consulta é contada uma vez só:

```bash
python scripts/summarize_access.py \
  --render-log evidencias/2026-11-05-logs-render.txt \
  --render-log evidencias/2026-11-12-logs-render.txt
```

Rodando a API no seu computador, o resumo lê o `logs/access.csv`:

```bash
python scripts/summarize_access.py
```

O resultado mostra o total de consultas úteis, o período observado e quanto cada rota recebeu. Guarde o resultado como evidência, sempre dizendo o período. Ficam de fora da conta `/`, `/health`, `/docs`, `/redoc` e `/openapi.json`, e só entram consultas `GET` que deram certo.

## Estrutura

```text
.
├── app/
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   └── routes.py
├── data/
├── docs/
├── evidencias/
├── scripts/
│   ├── export_gold.py
│   └── summarize_access.py
├── tests/
├── pytest.ini
├── README.md
├── plano-de-acao.md
├── diario-de-bordo.md
├── evidencias.csv
├── marco-1.md
├── marco-2.md
├── marco-3.md
├── socializacao.md
├── Dockerfile
└── docker-compose.yml
```
