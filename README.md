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

- API FastAPI implementada localmente;
- documentação OpenAPI automática em `/docs`;
- exportador que gera um banco DuckDB compacto a partir da camada Gold;
- rotas de municípios, indicadores municipais, rodovias, trechos críticos e acidentes;
- testes automatizados;
- registro técnico de acessos sem armazenar nome, e-mail ou IP;
- publicação pública: **pendente** — deve estar concluída antes do Marco 2.

### Endereços

- Local: `http://localhost:8000`
- Documentação local: `http://localhost:8000/docs`
- Endereço público: https://api-seguranca-viaria-ce.onrender.com
- Documentação interativa: https://api-seguranca-viaria-ce.onrender.com/docs
- Status da API: https://api-seguranca-viaria-ce.onrender.com/health
- Monitoramento de disponibilidade: UptimeRobot, com verificação do `/health` a cada 5 minutos
- Repositório da equipe: https://github.com/ayurireiscentraldedados/interface-grafica

## Como usar agora

### 1. Preparar o ambiente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Gerar o banco compacto da API

Com o projeto principal disponível ao lado deste repositório:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

Ou:

```bash
make export SOURCE_DB=../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

### 3. Iniciar a API

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Testar uma consulta

```bash
curl 'http://localhost:8000/api/v1/municipios?ano=2025'
```

A resposta tem esta forma:

```json
{
  "count": 2,
  "filters": {"ano": 2025},
  "data": [
    {
      "ibge_code": "2304400",
      "municipality": "Fortaleza"
    }
  ]
}
```

> O exemplo acima mostra o **formato** da resposta. O conteúdo retornado pelo serviço real depende da versão do banco exportado da camada Gold.

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
curl 'http://localhost:8000/'
```

## `GET /health`

**O que faz:** informa se a API está ativa e se o banco analítico está disponível.

**Exemplo:**

```bash
curl 'http://localhost:8000/health'
```

**Possíveis respostas:**

- `status=ok`: banco carregado;
- `status=degraded`: API subiu, mas o banco ainda não foi exportado.

## `GET /api/v1/datasets`

**O que faz:** lista os datasets realmente disponíveis no banco publicado e suas colunas.

**Parâmetros:** nenhum.

```bash
curl 'http://localhost:8000/api/v1/datasets'
```

## `GET /api/v1/municipios`

**O que faz:** lista os municípios disponíveis no recorte analítico.

**Parâmetros:**

- `ano` — opcional;
- `limit` — 1 a 500, padrão 184.

```bash
curl 'http://localhost:8000/api/v1/municipios?ano=2025'
```

**Erros possíveis:**

- `422`: parâmetro inválido;
- `503`: banco/dataset ainda não disponível.

## `GET /api/v1/municipios/{codigo_ibge}/indicadores`

**O que faz:** devolve os indicadores anuais do município identificado pelo código IBGE.

**Parâmetros:**

- `codigo_ibge` — obrigatório no caminho;
- `ano` — opcional.

```bash
curl 'http://localhost:8000/api/v1/municipios/2304400/indicadores?ano=2025'
```

**Erros possíveis:**

- `404`: combinação município/ano não encontrada;
- `422`: ano fora da faixa aceita;
- `503`: banco/dataset indisponível.

## `GET /api/v1/rodovias`

**O que faz:** lista/rankeia rodovias pelos indicadores observados na camada Gold.

**Parâmetros:**

- `ano` — opcional;
- `limit` — 1 a 100, padrão 20.

```bash
curl 'http://localhost:8000/api/v1/rodovias?ano=2025&limit=10'
```

## `GET /api/v1/trechos-criticos`

**O que faz:** lista trechos rodoviários agregados em segmentos de 10 km.

**Parâmetros:**

- `ano` — opcional;
- `rodovia` — opcional;
- `limit` — 1 a 100.

```bash
curl 'http://localhost:8000/api/v1/trechos-criticos?ano=2025&limit=10'
```

## `GET /api/v1/acidentes`

**O que faz:** consulta ocorrências da mart de mapa com paginação simples.

**Parâmetros:**

- `ano` — opcional;
- `municipio` — opcional;
- `limit` — 1 a 500, padrão 100;
- `offset` — início da página, padrão 0.

```bash
curl 'http://localhost:8000/api/v1/acidentes?ano=2025&municipio=Fortaleza&limit=50'
```

## Como rodar localmente com Docker

Primeiro gere `data/ceara_road_safety_api.duckdb`. Depois:

```bash
docker compose up --build -d
```

Confira:

```bash
curl 'http://localhost:8000/health'
```

Documentação:

```text
http://localhost:8000/docs
```

Parar:

```bash
docker compose down
```

## Testes automatizados

Os testes usam um DuckDB temporário criado exclusivamente para a suíte; os números da fixture **não são dados reais do projeto**.

```bash
pytest -q
```

ou:

```bash
make test
```

## Evidência de alcance

A API registra somente:

```text
timestamp UTC, método HTTP, caminho, status e duração
```

Ela **não registra nome, e-mail ou IP** para a evidência da disciplina.

Para resumir consultas úteis:

```bash
python scripts/summarize_access.py
```

O resultado pode ser salvo como evidência de contagem, sempre informando o período observado. Requisições de `/health`, `/docs`, `/redoc` e `/openapi.json` são excluídas do resumo.

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
