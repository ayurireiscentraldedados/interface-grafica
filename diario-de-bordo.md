# Diário de bordo

> Regra: registrar fatos reais na semana em que ocorrerem. Não reconstruir retroativamente atividades que não estão sustentadas por commit, mensagem, reunião ou arquivo.

### Semana de 18/09

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 1h; Victor Cavalcante Pena — 1h; Felipe dos Reis Pena — 1h; Eduardo Rodrigues Bezerra Loiola — 1h; Jorge Leão Salgado Neto — 1h

**O que foi feito:**

- Realizamos a primeira reunião da equipe para discutir a proposta do projeto, alinhar as ideias iniciais e definir como seria o desenvolvimento do trabalho.
- Criamos e organizamos o repositório do projeto no GitHub e estruturamos o Diário de Bordo para registrar as atividades, evidências e horas de trabalho da equipe.

**Obstáculo:** Nenhum obstáculo relevante. A reunião foi utilizada principalmente para o planejamento inicial e a organização da equipe.

**Contato com o público:** Não houve contato com o público nesta semana. A atividade foi exclusivamente de planejamento e organização interna da equipe.

**Evidência coletada:** Registro da criação e organização do repositório no GitHub e do arquivo de Diário de Bordo, armazenados no próprio repositório da equipe.

**Próxima semana:** Definir com mais detalhes o escopo do projeto, dividir as primeiras tarefas entre os integrantes e iniciar a execução das atividades planejadas.

---

### Semana de 25/09

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h

**O que foi feito:**

- Upload dos instrumentos-modelo da disciplina para o repositório e revisão inicial da estrutura do diário de bordo para uso da equipe (commits `3ea102a` e `e6751ab`).
- Organização das branches e alinhamento inicial do fluxo de versionamento no GitHub.

**Obstáculo:** Dificuldade inicial em fechar qual recorte da plataforma principal de segurança viária seria exposto sem depender de todo o pipeline pesado de ETL.

**Contato com o público:** Não houve contato com o público externo nesta semana.

**Evidência coletada:** Commits `3ea102a` e `e6751ab` no histórico do repositório.

**Próxima semana:** Fechar o escopo enxuto da Trilha A (API pública de dados abertos) e publicar a estrutura inicial do serviço.

---

### Semana de 07/10

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Victor Cavalcante Pena — 4h; Felipe dos Reis Pena — 2h; Eduardo Rodrigues Bezerra Loiola — 1h; Jorge Leão Salgado Neto — 1h

**O que foi feito:**

- [x] Redefinimos o escopo para uma API pública independente do dashboard, reutilizando a camada Gold da plataforma de segurança viária.
- [x] Integramos o scaffold FastAPI ao repositório da disciplina (`app/main.py`, `app/routes.py`, `app/db.py`).
- [x] Geramos um DuckDB compacto com `scripts/export_gold.py` e publicamos na release `data-2026-08-v1`.
- [x] Executamos a suíte `pytest -q` e configuramos o GitHub Actions (`.github/workflows/ci.yml`).
- [x] Revisamos `plano-de-acao.md`, `README.md` e distribuímos os papéis (Ayuri responsável por documentação, clareza do `/docs` e revisão do teste do estranho).
- [x] Publicamos o endereço público no Render (`https://api-seguranca-viaria-ce.onrender.com`) e definimos perfis externos para os testes.

**Obstáculo:** Entendimento inicial do fluxo de empacotamento do DuckDB para a nuvem gratuita sem acoplar o ETL completo da plataforma principal.

**Contato com o público:** Ainda não houve teste externo executado nesta semana; foi feita a preparação do roteiro em `docs/ROTEIRO-TESTE-EXTERNO.md`.

**Evidência coletada:** Commits `bf5ef69`, `aeb7509`, `dbe5e39`, `9b42f54`, `f39c0f3`, `4bbdf89` e tag `data-2026-08-v1`.

**Próxima semana:** Expandir as rotas analíticas, preparar formulário/convites para usuários externos e iniciar a coleta de logs de acesso.

---

### Semana de 14/10

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h; Felipe dos Reis Pena — 4h; Eduardo Rodrigues Bezerra Loiola — 3h; Jorge Leão Salgado Neto — 2h

**O que foi feito:**

- Implementação e revisão das novas rotas de análise: `/api/v1/municipios/risco-per-capita`, `/api/v1/analises/circunstancias` e `/api/v1/analises/perfil-rodovia` (commits `54f61e7` a `a1c862c`), além de `/api/v1/analises/evolucao` e `/api/v1/analises/quando-acontece` (commit `eb03506`).
- Registro de acessos também na saída padrão (`ACESSO ...`) para leitura nos logs do Render (commit `256a6ca`).
- Criação de formulário de pesquisa técnica para avaliação por usuários externos e revisão da documentação das novas rotas no `README.md` (organização e revisão conduzidas com apoio de Ayuri).

**Obstáculo:** O armazenamento local do Render gratuito é efêmero a cada reinício; por isso o middleware passou a gravar também linhas estruturadas `ACESSO` no stdout do serviço.

**Contato com o público:** Envio inicial do link público e abertura do formulário de feedback técnico (`https://docs.google.com/forms/d/e/1FAIpQLSd91nFu0ggNuwoBgZqxoXoMKLha7jGSmQ1hYihQPFp6WCMYfQ/viewform`).

**Evidência coletada:** Pull requests `#1` (`9654174`) e `#2` (`d00f52f`), commits na branch `dev-jorge` (`76e3c30`, `f8cb982`, `0dafe8f`, `fc2ef4f`) e primeiros registros em `evidencias/2026-11-12-logs-render.txt`.

**Próxima semana:** Aplicar o roteiro do "teste do estranho" sem orientação prévia e registrar as dificuldades reais de uso da documentação.

---

### Semana de 21/10

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Felipe dos Reis Pena — 2h

**O que foi feito:**

- Execução e documentação do primeiro teste sem orientação com estudante externo à disciplina (`evidencias/2026-10-23-teste-externo-01.md`), conduzido por Ayuri conforme `docs/ROTEIRO-TESTE-EXTERNO.md`.
- Identificação de fricção na rota `/api/v1/municipios/{ibge_code}/indicadores` (usuário tentou informar o nome do município no lugar do código IBGE `2304400`) e dúvida sobre o formato de `rodovia` (`116` vs. `BR-116`).
- Organização das contribuições parciais da equipe no repositório (`f154ee3` e `e4449e0`).

**Obstáculo:** Usuários que abrem diretamente o `/docs` sem ler o `README.md` inteiro sentiam falta de exemplos de códigos IBGE e de explicação dos parâmetros na própria interface Swagger.

**Contato com o público:** 1º teste externo sem orientação realizado em 23/10 com estudante de graduação externo à turma.

**Evidência coletada:** `evidencias/2026-10-23-teste-externo-01.md` e linha correspondente em `evidencias.csv`.

**Próxima semana:** Planejar ajustes na documentação interativa `/docs` e acompanhar novas consultas externas à API.

---

### Semana de 28/10

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h

**O que foi feito:**

- Acompanhamento da disponibilidade da URL pública (`https://api-seguranca-viaria-ce.onrender.com/health`) e verificação das consultas registradas nos endpoints de municípios, rodovias e trechos críticos.
- Revisão dos textos de limitações dos dados no `README.md` (recorte restrito a rodovias federais da PRF, instabilidade de taxas per capita em municípios pequenos e ano de 2026 parcial até 31/08/2026).

**Obstáculo:** Baixa adesão espontânea por formulário aberto sem convite individual; decidimos abordar diretamente perfis específicos do público-alvo (comunicação/jornalismo e desenvolvimento web) para observar o uso real.

**Contato com o público:** Convites diretos enviados para novos testadores externos avaliarem a URL pública.

**Evidência coletada:** Registros de acesso de 29/10 consolidados em `evidencias/2026-11-12-logs-render.txt`.

**Próxima semana:** Realizar segundo ciclo de teste externo e coletar feedback sobre uso prático dos dados.

---

### Semana de 04/11

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Jorge Leão Salgado Neto — 1h

**O que foi feito:**

- Realização e registro do segundo teste com público externo em 06/11 (`evidencias/2026-11-06-teste-externo-02.md`), com estudante de comunicação/jornalismo interessado em dados de mobilidade.
- Mapeamento do obstáculo de *cold start* da instância gratuita do Render (cerca de 35 segundos na primeira requisição após inatividade) e dúvida sobre a comparação do ano parcial de 2026.

**Obstáculo:** O tempo de despertar (*cold start*) do plano gratuito do Render fez a pessoa testadora achar inicialmente que o link estava fora do ar no primeiro clique.

**Contato com o público:** 2º teste externo documentado em 06/11 (formulário + conversa de acompanhamento).

**Evidência coletada:** `evidencias/2026-11-06-teste-externo-02.md` e linha correspondente em `evidencias.csv`.

**Próxima semana:** Preparar Marco 2, realizar terceiro teste externo e consolidar a contagem de acessos.

---

### Semana de 11/11 — Marco 2 em 13/11

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h

**O que foi feito:**

- Condução do terceiro teste externo sem orientação em 12/11 com desenvolvedor web externo (`evidencias/2026-11-12-teste-externo-03.md`).
- Extração e consolidação das linhas de acesso da API com `scripts/summarize_access.py`, totalizando 41 consultas úteis bem-sucedidas (`evidencias/2026-11-12-logs-render.txt` e `evidencias/2026-11-12-resumo-acessos.md`).
- Conferência das rotas públicas no ar (`https://api-seguranca-viaria-ce.onrender.com/docs` e `/health`).

**Obstáculo:** As atualizações documentais do Marco 2, a consolidação do `evidencias.csv` e o preenchimento do `marco-2.md` não haviam sido enviados para a branch `main` antes da verificação assíncrona do professor (que ocorreu sem encontro presencial na sexta-feira).

**Contato com o público:** 3º teste externo realizado em 12/11 com desenvolvedor web externo.

**Evidência coletada:** `evidencias/2026-11-12-teste-externo-03.md`, `evidencias/2026-11-12-logs-render.txt` e `evidencias/2026-11-12-resumo-acessos.md`.

**Próxima semana:** Incorporar devolutiva do Marco 2, subir todas as evidências, atualizar `/docs` com as melhorias pedidas pelos testadores e fechar a entrega do Marco 2 na `main`.

---

### Semana de 18/11

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 4h

**O que foi feito:**

- Melhoria direta na clareza da documentação interativa `/docs` (`app/main.py` e `app/routes.py`), atendendo às dificuldades reais registradas nos testes externos: inclusão do guia **"Como começar sem ajuda"** no topo do Swagger, organização das rotas em `openapi_tags` (`meta`, `consultas`, `analises`) e adição de descrições e exemplos explícitos em todos os parâmetros (`ibge_code=2304400`, `rodovia` aceitando `116` ou `BR-116`, alerta de recorte parcial de `2026`).
- Adição de testes automatizados em `tests/test_api.py` para garantir que o schema `/openapi.json` mantenha as tags, instruções iniciais e descrições de parâmetros (`94 passed`).
- Preenchimento completo do `marco-2.md`, atualização do `evidencias.csv`, revisão do `docs/CHECKLIST-MARCO-2.md` e consolidação deste `diario-de-bordo.md` na branch `main`.

**Obstáculo:** Sincronização desigual de entregas entre integrantes da equipe; para não comprometer o registro do projeto e da etapa de documentação/experiência de uso, toda a frente de documentação, `/docs`, testes externos, evidências e ficha do Marco 2 foi consolidada e subida diretamente na `main`.

**Contato com o público:** Consolidação e anonimização por vínculo dos 3 testes externos em `evidencias/` e `evidencias.csv`.

**Evidência coletada:** `marco-2.md`, `evidencias.csv`, arquivos em `evidencias/` e commits de melhoria do `/docs` e da documentação na `main`.

**Próxima semana:** Fechar documentação final e preparar o Marco 3.

---

### Semana de 25/11 — Marco 3 em 27/11

**Quem trabalhou e quanto:** [PREENCHER NA SEMANA]

**O que foi feito:** [PREENCHER NA SEMANA]

**Obstáculo:** [PREENCHER NA SEMANA]

**Contato com o público:** [PREENCHER NA SEMANA]

**Evidência coletada:** [PREENCHER NA SEMANA]

**Próxima semana:** ensaiar socialização e preparar autoavaliações individuais.

---

### Semana de 02/12 — Socialização em 04/12

**Quem trabalhou e quanto:** [PREENCHER NA SEMANA]

**O que foi feito:** [PREENCHER NA SEMANA]

**Obstáculo:** [PREENCHER NA SEMANA]

**Contato com o público:** [PREENCHER NA SEMANA]

**Evidência coletada:** [PREENCHER NA SEMANA]

**Próxima semana:** registrar o que fica publicado e encerrar a ação.
