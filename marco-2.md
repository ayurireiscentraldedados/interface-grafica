# Marco 2 — 13/11/2026 (consolidado na `main` em 16/11/2026)

## Identificação

- **Equipe:** Ayuri de Souza dos Reis; Victor Cavalcante Pena; Felipe dos Reis Pena; Eduardo Rodrigues Bezerra Loiola; Jorge Leão Salgado Neto.
- **Marco e data:** Marco 2 — 13/11/2026 (entrega consolidada dentro do prazo de ajuste até 22/11/2026).
- **Trilha:** A — API pública de dados abertos.
- **Endereço público do produto:** https://api-seguranca-viaria-ce.onrender.com (documentação interativa em https://api-seguranca-viaria-ce.onrender.com/docs e verificação de saúde em https://api-seguranca-viaria-ce.onrender.com/health).
- **Commit ou tag desta entrega:** tag `marco-2` (branch `main`).

## Campo 1 — O que funciona hoje

Testes executados diretamente contra o endereço público `https://api-seguranca-viaria-ce.onrender.com`:

1. **Testar as rotas pelo navegador sem ajuda da equipe:**
   Abrir `https://api-seguranca-viaria-ce.onrender.com/docs`, visualizar a documentação interativa com as rotas da API, clicar em `GET /api/v1/datasets` → *Try it out* → *Execute* e receber a lista dos 7 conjuntos de dados carregados no banco (`mart_municipality_road_safety_yearly`, `mart_highway_safety`, `mart_highway_segment_safety`, `mart_accident_map`, `mart_weather_road_safety_pt`, `mart_vehicle_road_safety` e `dim_municipality`).
2. **Consultar os indicadores anuais de Fortaleza (código IBGE `2304400`) em 2025:**
   Rodar no terminal:
   ```bash
   curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios/2304400/indicadores?ano=2025'
   ```
   E receber em JSON os indicadores de Fortaleza em 2025: população estimada de `2578483`, `299` acidentes (`11.6` por 100 mil hab.), `15` acidentes fatais, `15` mortes (`0.58` por 100 mil hab.), `71` feridos graves (`2.75` por 100 mil hab.) e `627` veículos envolvidos.
3. **Consultar os trechos críticos de 10 km nas rodovias federais do Ceará em 2025:**
   Rodar no terminal:
   ```bash
   curl 'https://api-seguranca-viaria-ce.onrender.com/api/v1/trechos-criticos?ano=2025&limit=3'
   ```
   E receber os três segmentos de 10 km com maior concentração observada em 2025: `BR-116 · km 0–10` (Fortaleza, `138` acidentes e `7` mortes), `BR-116 · km 10–20` (Fortaleza, `97` acidentes e `5` mortes) e `BR-222 · km 0–10` (Fortaleza, `60` acidentes e `3` mortes).

Além das rotas já ativas na URL pública, o código na `main` conta com 5 rotas analíticas adicionais (`/api/v1/municipios/risco-per-capita`, `/api/v1/analises/circunstancias`, `/api/v1/analises/perfil-rodovia`, `/api/v1/analises/evolucao` e `/api/v1/analises/quando-acontece`) e melhorias de usabilidade no `/docs`, todas cobertas por `94` testes automatizados (`python -m pytest -q`).

## Campo 2 — O que mudou desde o Marco 1

- **Passou a existir:**
  - Serviço FastAPI completo (`app/`) conectado ao banco DuckDB compacto exportado da camada Gold (`data-2026-08-v1`, cobrindo 2024, 2025 e 2026 até 31/08/2026) e publicado em `https://api-seguranca-viaria-ce.onrender.com`.
  - Rotas de consulta (`/api/v1/datasets`, `/api/v1/municipios`, `/api/v1/municipios/{ibge_code}/indicadores`, `/api/v1/rodovias`, `/api/v1/trechos-criticos`, `/api/v1/acidentes`) e cinco rotas de análise (`/api/v1/municipios/risco-per-capita`, `/api/v1/analises/circunstancias`, `/api/v1/analises/perfil-rodovia`, `/api/v1/analises/evolucao`, `/api/v1/analises/quando-acontece`).
  - Documentação interativa `/docs` aprimorada com seção **"Como começar sem ajuda"**, agrupamento por `openapi_tags` (`meta`, `consultas`, `analises`) e descrições/exemplos em todos os parâmetros a partir das dúvidas reais do público externo.
  - Suíte com `94` testes automatizados (`tests/test_api.py` e `tests/test_export.py`) executada a cada push via GitHub Actions (`.github/workflows/ci.yml`).
  - Registro de acessos sem dados pessoais no stdout do serviço (`ACESSO ...`) + script `scripts/summarize_access.py` e consolidação das evidências em `evidencias/` e `evidencias.csv`.
- **Foi cortado, e por quê:**
  - **Execução do pipeline ETL completo (PRF, IBGE e Open-Meteo) em tempo de requisição:** cortado para não inviabilizar o tempo de resposta e a memória do plano gratuito no Render; a API consome o pacote analítico já validado e exportado (`ceara_road_safety_api.duckdb`, ~2,9 MB).
  - **Dimensões sem coluna correspondente no banco compacto atual (`causa`, `tipo_acidente` e `condicao_pista` em `/analises/circunstancias`, e `tipo_veiculo` em `/analises/perfil-rodovia`):** em vez de remover as rotas ou expor dados incompletos silenciosamente, a API informa explicitamente `503` ou lista o campo em `dimensoes_indisponiveis` até que uma nova exportação da plataforma principal inclua essas colunas.

## Campo 3 — Alcance

| Indicador | Planejado | Obtido até hoje | Onde está a evidência |
| :-- | :-- | :-- | :-- |
| consultas úteis bem-sucedidas | ≥ 30 até 27/11 | **41 consultas úteis** (`GET` `2xx` em `/api/v1/*`, excluindo `/health` e `/docs`, entre 14/10 e 12/11) | `evidencias/2026-11-12-resumo-acessos.md` e `evidencias/2026-11-12-logs-render.txt` |
| pessoas externas testando | ≥ 3 até 27/11 | **3 pessoas externas** testaram sem orientação prévia (estudante de tecnologia, estudante de jornalismo e desenvolvedor web) | `evidencias/2026-10-23-teste-externo-01.md`, `evidencias/2026-11-06-teste-externo-02.md` e `evidencias/2026-11-12-teste-externo-03.md` |

**O que o público externo disse:**
- *"Pelo `/docs` deu para testar tudo direto no navegador sem instalar nada, mas na rota de indicadores por município tentei digitar o nome da cidade antes de ver que pedia o código do IBGE."* (estudante de graduação externo à turma, em `evidencias/2026-10-23-teste-externo-01.md`).
- *"Ter os trechos de 10 km já somados por rodovia poupa horas de planilha para uma pauta, só achei que o link estava fora no primeiro clique porque demorou meio minuto para acordar."* (estudante de comunicação/jornalismo, em `evidencias/2026-11-06-teste-externo-02.md`).

## Campo 4 — Obstáculo e replanejamento

1. **Fricção no primeiro uso do `/docs` sem ler o README (~2h):** no primeiro teste externo (23/10), a pessoa tentou passar `"Fortaleza"` em `/api/v1/municipios/{ibge_code}/indicadores` e ficou em dúvida se `rodovia` aceitava `116` ou `BR-116`. **Decisão:** incluímos orientações iniciais, exemplos de códigos IBGE (`2304400`) e explicação de todos os parâmetros direto no schema OpenAPI do `/docs` (`app/main.py` e `app/routes.py`), além do `README.md`.
2. **Hibernação (*cold start*) e disco efêmero no plano gratuito do Render (~3h):** a instância gratuita leva ~35s para responder ao primeiro acesso após inatividade e apaga arquivos locais em novos deploys. **Decisão:** gravamos os acessos também no log de saída do serviço (`ACESSO ...`) para consolidação com `scripts/summarize_access.py` e configuramos verificação periódica do `/health`.
3. **Atraso na consolidação documental na branch `main` (~3h):** parte dos registros semanais e do preenchimento do Marco 2 ficou dispersa ou não havia subido para a `main` até 13/11. **Decisão:** consolidamos todas as semanas do `diario-de-bordo.md`, os registros em `evidencias/`, o `evidencias.csv` e o `marco-2.md` diretamente na `main`.

## Campo 5 — Autopontuação

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | | 2 | API pública no ar com dados reais, tratamento explícito de erros (`404`, `422`, `503`), CI ativo e 94 testes automatizados passando. |
| D2 Alcance e adequação ao público | | 2 | 3 testes externos sem orientação documentados e 41 consultas úteis contabilizadas, gerando melhorias reais no `/docs` e no `README.md`. |
| D3 Documentação e reprodutibilidade | | 2 | `README.md` e `/docs` detalham público, exemplos executáveis, procedência, licenças, limitações dos dados e instruções locais/Docker. |
| D4 Registro do processo | | 1.5 | Diário, `evidencias.csv` e `marco-2.md` estão completos e sustentados por artefatos, mas a consolidação na `main` ocorreu após a primeira checagem de 13/11. |
| D5 Autoavaliação e reflexão | sim | — | autoavaliação individual é consolidada no encerramento. |

## Checklist

- [x] URL abre fora da máquina da equipe.
- [x] `/docs` foi testado no dia.
- [x] README corresponde à versão publicada.
- [x] Diário está semanalmente atualizado.
- [x] Evidências têm arquivo, data e vínculo do público.
- [x] Commit/tag do marco está no GitHub.
