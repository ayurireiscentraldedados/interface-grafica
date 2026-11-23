# Segurança Viária CE

**Dados de acidentes nas rodovias federais do Ceará, com consulta simples no navegador e API pública para reutilização.** A iniciativa acadêmica da UFC, na Trilha A de dados abertos, utiliza como infraestrutura a camada Gold do **Ceará Road Safety Data Platform**, que prepara dados da PRF, IBGE e Open-Meteo.

## Comece por aqui

| Objetivo | Acesso |
| :-- | :-- |
| **Consultar sem programar**: município, rodovias e trechos de 10 km | [Interface /explorar](https://api-seguranca-viaria-ce.onrender.com/explorar) |
| **Explorar os endpoints JSON** e seus parâmetros | [Swagger /docs](https://api-seguranca-viaria-ce.onrender.com/docs) |
| **Conferir o estado da API e do banco** | [Status /health](https://api-seguranca-viaria-ce.onrender.com/health) |
| **Sugerir melhorias ou comunicar problemas** | [GitHub Issues](https://github.com/ayurireiscentraldedados/interface-grafica/issues) |

**Sobre a publicação:** a interface `/explorar` e o redirecionamento da página inicial fazem parte do código desta versão. Para aparecerem no Render, a alteração precisa ser integrada à branch implantada e o deploy precisa terminar. Confirme a URL antes de convidar pessoas externas para testar.

## Para quem é

Estudantes, jornalistas de dados, pesquisadores e pessoas interessadas em mobilidade e segurança viária. A interface visual não exige cadastro, código IBGE, comandos de terminal ou conhecimento de JSON; os endpoints técnicos continuam disponíveis para integração com outros sistemas.

## Funcionalidades implementadas

- **Consulta guiada em `/explorar`:** busca de municípios por nome, seleção de ano, indicadores de acidentes, mortes e feridos graves, ranking de rodovias e lista de trechos de 10 km com mais ocorrências.
- **API em `/api/v1`:** datasets, municípios, indicadores municipais, rodovias, trechos críticos e acidentes.
- **Análises agregadas:** risco por 100 mil habitantes, circunstâncias, perfil de rodovias, evolução temporal, dia e hora, clima, veículos e regiões do IBGE.
- **Documentação interativa**, testes automatizados no GitHub Actions, verificação HTTP do serviço publicado e registros de acesso com data/hora, método, rota, status e duração (sem guardar IP, nome ou e-mail no log da aplicação).

A interface visual consulta os **mesmos endpoints JSON**: não mantém uma segunda base nem cria indicadores independentes.

### O que acontece ao abrir a página inicial?

- **Navegador:** se enviar `Accept: text/html`, `GET /` responde com redirecionamento **307** para `/explorar`.
- **Cliente de API:** se solicitar JSON, `GET /` devolve os caminhos da interface, do Swagger, do status e da API.
- As rotas `/docs`, `/health` e `/api/v1/...` continuam disponíveis.

### Dados e limites

O pacote atualmente documentado é [`data-2026-08-v1`](https://github.com/ayurireiscentraldedados/interface-grafica/releases/tag/data-2026-08-v1), com **2024 e 2025 completos** e **2026 parcial até 31/08/2026**. Não se trata de monitoramento em tempo real.

O recorte principal inclui acidentes **registrados pela PRF em rodovias federais** — não todos os acidentes do Ceará. Os rankings apresentam **contagens observadas**, não probabilidade de acidente nem risco comparável por viagem, pois não há denominadores de tráfego. Veja as limitações detalhadas abaixo.

## Como usar agora

### Consultas técnicas: Swagger, terminal e Python

Para consultar sem programação, use `/explorar`. Os exemplos abaixo servem a quem quer ler os dados em JSON ou integrar a API a outro programa.

**No navegador (Swagger).** Abra https://api-seguranca-viaria-ce.onrender.com/docs, escolha uma rota, clique em "Try it out" e em "Execute". Você também pode acessar uma URL diretamente, por exemplo:

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

Precisa de Python 3.13 (versão em `.python-version`). Rode todos os comandos abaixo a partir da **pasta raiz do projeto** (a que contém `app/` e `README.md`), porque o caminho do banco (`data/ceara_road_safety_api.duckdb`) é relativo a ela.

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
mkdir -p data
curl -fL --show-error -o data/ceara_road_safety_api.duckdb \
  https://github.com/ayurireiscentraldedados/interface-grafica/releases/download/data-2026-08-v1/ceara_road_safety_api.duckdb
```

No PowerShell do Windows, use `curl.exe` no lugar de `curl`.

Quem tem o projeto principal (Ceará Road Safety Data Platform) ao lado deste repositório também pode gerar o banco do zero:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

Ou, em Linux/macOS (o `make` não vem instalado no Windows; lá, use o comando `python` acima):

```bash
make export SOURCE_DB=../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

**3. Iniciar a API**

```bash
uvicorn app.main:app --reload --port 8000
```

**4. Abrir a interface e testar uma consulta**

- Interface simples: http://127.0.0.1:8000/explorar
- Swagger: http://127.0.0.1:8000/docs
- Status: http://127.0.0.1:8000/health

Para consultar diretamente os dados JSON:

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
- A análise por condição do tempo mostra em que tempo os acidentes registrados aconteceram, não se chuva é mais perigosa: faltam as horas e as viagens feitas com e sem chuva. A condição vem do Open-Meteo (estimativa para o horário e o local) e diverge bastante da anotada pelo policial: no banco publicado, o Open-Meteo aponta precipitação em 831 dos 3.559 acidentes (23%), e a PRF registra chuva ou garoa em 243 (7%).
- Na análise por tipo de veículo, mortes e feridos são contados por veículo, entre os seus ocupantes. O total de mortes (386) fica abaixo do total da base (472); a diferença provavelmente são vítimas sem veículo associado, como pedestres, mas isso precisa ser confirmado na plataforma principal.
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

**O que faz:** abre `/explorar` quando acessado no navegador (requisição com `Accept: text/html`). Clientes HTTP que solicitam JSON continuam recebendo os caminhos da API, incluindo `explorar` e `docs`.

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
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios/risco-per-capita?ano=2025&ordenar_por=mortes&limit=10'
```

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
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/circunstancias?dimensao=iluminacao&ano=2025'
```

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
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/perfil-rodovia?ano=2025&ordenar_por=mortes_por_100_acidentes&min_acidentes=50'
```

Cada perfil traz `posicao`, `acidentes`, `mortes`, `feridos_graves`, `mortes_por_100_acidentes`, `pct_acidentes_fatais`, `predominantes` (a categoria mais frequente de `horario`, `clima` e `tipo_veiculo`), `distribuicoes` (as 3 categorias mais frequentes, com contagem e percentual) e `trechos_criticos` (`km_inicial`, `km_final`, `acidentes`, `mortes`).

`pct_acidentes_fatais` e `distribuicoes` vêm das ocorrências mapeadas (`ocorrencias_mapeadas`), que podem divergir dos totais da tabela de rodovias. Dimensões ausentes no banco publicado são listadas em `dimensoes_indisponiveis` e omitidas do perfil. No banco publicado hoje, `tipo_veiculo` aparece como indisponível, porque a tabela de ocorrências não traz o tipo de veículo; para o Ceará inteiro, os tipos de veículo estão em `/api/v1/analises/veiculos`. Também existe uma "rodovia" chamada `0` (14 ocorrências), que parece ser registro sem rodovia identificada; confirme na plataforma antes de citá-la.

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
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/evolucao?granularidade=mes&municipio=Fortaleza&ano=2026'
```

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
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/quando-acontece?ano=2025&faixa=turno'
```

A resposta traz:

- `data`: a grade completa (7 dias × as faixas), **incluindo as células com zero**, sempre na mesma ordem (segunda a domingo, faixas do começo ao fim do dia). Cada célula tem `dia_semana`, `dia_semana_num` (1 = segunda), `faixa`, `acidentes`, `mortes`, `acidentes_fatais`, `taxa_fatal_pct` e `pct_do_total`;
- `por_dia_semana` e `por_faixa`: os totais de cada dia e de cada faixa;
- `mais_criticos`: até 5 células, ordenadas por mortes e depois por acidentes;
- `total_acidentes`, `total_mortes` e `sem_horario` (ocorrências sem data ou hora, que ficam fora das células).

Se a tabela tiver data mas não tiver hora, `faixa` aparece em `dimensoes_indisponiveis`. Nesse caso `data` e `por_faixa` vêm vazios e `count` vem 0; ficam preenchidos só `por_dia_semana` e `mais_criticos` (os dias mais críticos).

**Erros possíveis:**

- `404`: município, rodovia ou ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, ou tabela de acidentes sem data da ocorrência.

## `GET /api/v1/analises/clima`

**O que faz:** mostra em que condição do tempo os acidentes aconteceram e qual foi a gravidade em cada uma. É a única rota que usa os dados do Open-Meteo: para cada acidente, a plataforma buscou a condição do tempo no horário e no local da ocorrência. Responde perguntas como "quantos acidentes aconteceram com chuva?" e "os acidentes com tempo seco são mais graves?". Quando `ano` é omitido, os anos são somados.

**Parâmetros:**

- `ano` — opcional;
- `ordenar_por` — `acidentes` (padrão), `mortes` ou `mortes_por_100_acidentes`;
- `min_acidentes` — mínimo de acidentes por condição para entrar em `data`, padrão 1; use um valor maior com `mortes_por_100_acidentes` para ignorar condições raras.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/clima?ano=2025'
```

A resposta traz:

- `data`: uma linha por condição (`Céu limpo`, `Nublado`, `Garoa`, `Chuva`...), com `categoria`, `codigo` (o nome do grupo em inglês, como `clear`), `com_precipitacao`, `acidentes`, `mortes`, `feridos_graves`, `acidentes_fatais`, `pct_dos_acidentes`, `mortes_por_100_acidentes`, `pct_acidentes_fatais` e `medias`;
- `medias`: temperatura (°C), umidade (%), precipitação (mm), visibilidade (km) e vento (km/h) médios no momento dos acidentes daquela condição. Ao somar anos, a média é ponderada pelo número de acidentes;
- `por_precipitacao`: o mesmo resumo em duas linhas, `Sem precipitação` e `Com precipitação`. Não é afetado por `min_acidentes`;
- `total_acidentes` e `total_mortes`, que batem com os totais de `/rodovias`.

**No banco publicado hoje:** 831 dos 3.559 acidentes (23%) aconteceram com precipitação, com 9,87 mortes a cada 100 acidentes, contra 14,3 nos acidentes sem precipitação. Isso **não** quer dizer que chuva é mais segura: a rota não sabe quantas horas choveu nem quanta gente estava na estrada. A visibilidade média de 2026 nos acidentes sem precipitação (43,6 km) é quase o dobro da de 2024 (23,7 km) e 2025 (26,9 km); parece mudança na fonte, e não no tempo, então não compare visibilidade entre anos sem confirmar na plataforma principal.

**Erros possíveis:**

- `404`: ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, tabela de clima ausente, ou ordenação por mortes numa tabela sem coluna de mortes.

## `GET /api/v1/analises/veiculos`

**O que faz:** lista os tipos de veículo envolvidos nos acidentes e o que aconteceu com os ocupantes de cada tipo. Responde perguntas como "que fatia das mortes é de motociclistas?" e "em qual tipo de veículo os ocupantes mais morrem?". Quando `ano` é omitido, os anos são somados.

**Parâmetros:**

- `ano` — opcional;
- `ordenar_por` — `veiculos` (padrão), `mortes`, `feridos_graves`, `mortes_por_100_veiculos` ou `feridos_graves_por_100_veiculos`;
- `min_veiculos` — mínimo de veículos envolvidos por tipo, padrão 1; use um valor maior com as taxas para ignorar tipos raros;
- `limit` — 1 a 50, padrão 20.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/veiculos?ano=2025&ordenar_por=mortes_por_100_veiculos&min_veiculos=100'
```

Cada item traz `tipo_veiculo`, `veiculos_envolvidos`, `acidentes`, `ocupantes`, `mortes`, `feridos_graves`, `feridos_leves`, `ilesos`, `pct_dos_veiculos`, `pct_das_mortes`, `mortes_por_100_veiculos`, `feridos_graves_por_100_veiculos` e `idade_media_veiculo` (em anos; `null` quando não se aplica, como em bicicleta). A resposta traz também `total_veiculos` e `total_mortes`, calculados antes de `min_veiculos` e `limit`.

**Como ler:**

- `mortes` e os feridos são dos ocupantes daquele tipo de veículo. Por isso `total_mortes` (386 no banco publicado) fica abaixo do total de `/rodovias` (472);
- um acidente entre uma moto e um carro entra em `acidentes` dos dois tipos. Não some a coluna `acidentes`;
- as taxas são por veículo envolvido em acidente, não por veículo em circulação. Sem o tamanho da frota e os km rodados, a rota não diz qual veículo é mais arriscado, só qual teve desfecho pior quando o acidente aconteceu.

**No banco publicado hoje:** as motocicletas são 28,5% dos veículos envolvidos e 54,9% das mortes.

**Erros possíveis:**

- `404`: ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, tabela de veículos ausente, ou ordenação por uma coluna (mortes ou feridos graves) que a tabela publicada não tem.

## `GET /api/v1/analises/regioes`

**O que faz:** compara as regiões do Ceará (divisão do IBGE) por acidentes, mortes e feridos graves, em números absolutos e a cada 100 mil habitantes. Responde perguntas como "qual região concentra mais acidentes?" e "onde se morre mais em relação ao tamanho da população?". Quando `ano` é omitido, os anos são somados.

**Parâmetros:**

- `nivel` — `intermediaria` (padrão, 6 regiões) ou `imediata` (18 regiões);
- `ano` — opcional;
- `ordenar_por` — `acidentes` (padrão), `mortes`, `feridos_graves`, `acidentes_por_100k`, `mortes_por_100k` ou `feridos_graves_por_100k`;
- `limit` — 1 a 50, padrão 20.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/analises/regioes?ano=2025&ordenar_por=mortes_por_100k'
```

Cada item traz `regiao`, `municipios` (quantos municípios a região tem), `acidentes`, `mortes`, `feridos_graves`, `pct_dos_acidentes`, `pct_das_mortes`, `mortes_por_100_acidentes`, `acidentes_por_100k`, `mortes_por_100k`, `feridos_graves_por_100k` e `municipio_com_mais_acidentes`. A resposta traz também `total_acidentes` e `total_mortes`, que batem com os totais de `/rodovias`.

**Como ler:**

- as taxas usam a população do IBGE da mart municipal. Com vários anos somados, a taxa é a média anual por 100 mil habitantes; como 2026 vai só até 31/08, use `ano` com um ano fechado (2024 ou 2025) para comparar;
- só entram acidentes de rodovias federais registrados pela PRF. Uma região com mais quilômetros de rodovia federal registra mais acidentes sem que isso diga algo sobre a população dela;
- regiões com pouca população e poucos acidentes têm taxas instáveis.

**No banco publicado hoje (2025, regiões intermediárias):** Fortaleza concentra 66% dos acidentes (864 de 1.302) e tem a maior taxa de acidentes (17,1 a cada 100 mil habitantes). Quixadá tem a maior taxa de mortes (2,8 a cada 100 mil), e Juazeiro do Norte tem 28 mortes a cada 100 acidentes, contra 10 em Fortaleza.

**Erros possíveis:**

- `404`: ano sem nenhum registro;
- `422`: parâmetro fora dos valores aceitos;
- `503`: banco indisponível, tabela municipal ausente, nível de região ausente na tabela, ou ordenação por uma coluna (mortes, feridos graves ou população) que a tabela publicada não tem.

## `GET /api/v1/rodovias`

**O que faz:** lista/rankeia rodovias pelos indicadores observados na camada Gold.

**Parâmetros:**

- `ano` — opcional;
- `limit` — 1 a 100, padrão 20.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/rodovias?ano=2025&limit=10'
```

O resultado vem ordenado do maior para o menor número de acidentes; em caso de empate, desempata por mortes e feridos graves, para a mesma consulta sempre devolver a mesma ordem.

**Erros possíveis:**

- `422`: `ano` ou `limit` fora da faixa aceita;
- `503`: banco/dataset indisponível.

## `GET /api/v1/trechos-criticos`

**O que faz:** lista trechos rodoviários agregados em segmentos de 10 km.

**Parâmetros:**

- `ano` — opcional;
- `rodovia` — opcional; aceita `116` ou `BR-116`;
- `limit` — 1 a 100, padrão 20.

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/trechos-criticos?ano=2025&rodovia=BR-116&limit=10'
```

O resultado vem ordenado pelo número de acidentes, com o mesmo desempate de `/rodovias`.

**Erros possíveis:**

- `422`: `ano` ou `limit` fora da faixa aceita;
- `503`: banco/dataset indisponível.

## `GET /api/v1/acidentes`

**O que faz:** consulta ocorrências da mart de mapa com paginação simples.

**Parâmetros:**

- `ano` — opcional;
- `municipio` — opcional; nome do município, sem diferenciar maiúsculas de minúsculas (ex.: `Fortaleza`, `sobral`);
- `limit` — 1 a 500, padrão 100;
- `offset` — início da página, padrão 0 (para a página seguinte, some o `limit` ao `offset`).

```bash
curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/acidentes?ano=2025&municipio=Fortaleza&limit=50'
```

A ordem é fixa, então páginas diferentes não repetem nem pulam ocorrências.

**Erros possíveis:**

- `422`: `ano`, `limit` ou `offset` fora da faixa aceita;
- `503`: banco/dataset indisponível.

## Como rodar localmente com Docker

Primeiro coloque o banco em `data/ceara_road_safety_api.duckdb`: baixe-o da release (passo 2 de "Rodar no seu computador") ou gere-o com `scripts/export_gold.py`. Depois:

```bash
docker compose up --build -d
```

Confira:

```bash
curl 'http://127.0.0.1:8000/health'
```

Abra a interface em `http://127.0.0.1:8000/explorar` ou a documentação técnica em `http://127.0.0.1:8000/docs`.

Parar:

```bash
docker compose down
```

## Testes automatizados

Os testes usam um DuckDB temporário criado exclusivamente para a suíte; os números da fixture **não são dados reais do projeto**.

```bash
python -m pytest -q
```

ou, em Linux/macOS:

```bash
make test
```

Os testes cobrem os casos que funcionam e também os erros: parâmetro inválido (`422`), município ou rodovia que não existe (`404`), banco ou tabela ausente (`503`) e banco com colunas diferentes do esperado (`500`). Os testes de `tests/test_explorar.py` verificam a página HTML, elementos básicos de acessibilidade, referências às rotas JSON e as respostas de `/` para navegador e cliente JSON. **Testes automatizados não substituem testes externos reais de usabilidade.**

### Testar a API que está no ar

Os testes acima usam dados inventados. Para conferir a API **pública** de verdade, existe o script `scripts/testar_api.py`. Ele faz chamadas HTTP reais ao endereço público e confere o que `/docs` e este README prometem: rotas de consulta e de análise, filtros, paginação, erros `422`/`404`/`405`, CORS e tempo de resposta. Usa só a biblioteca padrão do Python, sem instalar nada além do próprio Python:

```bash
python scripts/testar_api.py
```

O Render gratuito "dorme" quando fica sem uso e a primeira resposta pode demorar quase um minuto. Se der erro de tempo esgotado, rode de novo com mais paciência:

```bash
python scripts/testar_api.py --timeout 90
```

No fim, o script mostra quantas verificações passaram e quantas falharam, e termina com código de saída `1` se alguma falhar. Rota que não existe na API pública aparece como "PULOU", não como falha.

## Validação com público externo — Marco 3

O teste de usabilidade deve ser feito **sem orientação** com pessoas externas à equipe, principalmente para verificar se alguém sem experiência com APIs consegue encontrar e interpretar informações na interface.

- **Site a testar:** https://api-seguranca-viaria-ce.onrender.com/explorar (confirmar previamente que o deploy publicado está atualizado).
- **[Formulário curto de usabilidade](https://docs.google.com/forms/d/e/1FAIpQLScYO5dqllE4L5dsXwMkozAsHMAAKx6R3SFJlDqfUKCRIJj8Kg/viewform):** registra conclusão das tarefas, nota de facilidade e sugestões.
- **Tarefas:** consultar Fortaleza em 2025, identificar a rodovia com mais acidentes, localizar um trecho de 10 km e reconhecer uma limitação dos dados.
- **Critérios previstos para o Marco 3:** pelo menos **três participantes externos com evidência primária verificável** e **duas melhorias ligadas a feedback real**, sem contar respostas de integrantes da equipe.
- **Passo a passo:** [`docs/VALIDACAO-EXPLORAR.md`](docs/VALIDACAO-EXPLORAR.md).

As **respostas originais do Forms e a planilha vinculada devem permanecer privadas**. Para o repositório, compartilhar somente evidências anonimizadas, observando a autorização para citar comentários. Registrar data, identificação anônima, versão/commit testado e melhorias realizadas. **Não preencher respostas pelos participantes nem afirmar que uma meta foi cumprida sem os comprovantes.**

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
│   ├── explorer.py                # Página /explorar
│   ├── main.py                    # FastAPI e rota /
│   ├── routes.py                  # API JSON /api/v1
│   └── static/
│       └── explorar.html         # Interface de consulta
├── data/                          # DuckDB local
├── docs/
│   └── VALIDACAO-EXPLORAR.md      # Protocolo de teste externo
├── evidencias/                    # Evidências compartilháveis e anonimizadas
├── scripts/
│   ├── auditar_evidencias.py
│   ├── export_gold.py
│   ├── instalar_explorar.py
│   ├── summarize_access.py
│   └── testar_api.py
├── tests/
│   ├── test_explorar.py
│   └── ...                        # Outros testes da API e da auditoria
├── pytest.ini
├── README.md
├── CONTRIBUTING.md
├── plano-de-acao.md
├── diario-de-bordo.md
├── evidencias.csv
├── marco-1.md
├── marco-2.md
├── marco-3.md
├── socializacao.md
├── autoavaliacao-<integrante>.md
├── Dockerfile
└── docker-compose.yml
```
