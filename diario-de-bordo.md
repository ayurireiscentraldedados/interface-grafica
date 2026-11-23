# Diário de bordo

> Regra: registrar fatos reais na semana em que ocorrerem. Não reconstruir retroativamente atividades que não estão sustentadas por commit, mensagem, reunião ou arquivo.
>
> **Nota de revisão (17/11/2026):** as semanas 1 a 10 foram conferidas contra o histórico do Git. Cada rota nova de análise passou a constar na semana do commit que a introduziu (as rotas de risco per capita, circunstâncias e perfil de rodovia em 13/10; clima e veículos em 16/11; regiões em 17/11). Nas semanas anteriores, o trabalho de Felipe aparece como pesquisa, sem atribuir rota que ainda não existia. As horas são as informadas por cada integrante.

## Índice das semanas

| Semana | Data | Destaque |
| --- | --- | --- |
| [1](#semana-1--18092026) | 18/09/2026 | Primeira reunião e criação do repositório |
| [2](#semana-2--25092026) | 25/09/2026 | Instrumentos-modelo e organização das branches |
| [3](#semana-3--02102026) | 02/10/2026 | Pesquisa de novas rotas |
| [4](#semana-4--09102026) | 09/10/2026 | API no ar no Render |
| [5](#semana-5--16102026) | 16/10/2026 | Novas rotas de análise e formulário de pesquisa |
| [6](#semana-6--23102026) | 23/10/2026 | 1º teste externo |
| [7](#semana-7--30102026) | 30/10/2026 | Convites diretos a testadores |
| [8](#semana-8--06112026) | 06/11/2026 | 2º teste externo |
| [9](#semana-9--13112026) | 13/11/2026 | **Marco 2**, 3º teste externo |
| [10](#semana-10--20112026) | 20/11/2026 (em andamento) | Melhoria do `/docs` e rotas `/analises/clima`, `/analises/veiculos` e `/analises/regioes` |
| [11](#semana-11--27112026) | 27/11/2026 | **Marco 3** |
| [12](#semana-12--04122026) | 04/12/2026 | **Socialização** |

---

## Semana 1 — 18/09/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 1h; Victor Cavalcante Pena — 1h; Felipe dos Reis Pena — 1h; Eduardo Rodrigues Bezerra Loiola — 1h; Jorge Leão Salgado Neto — 1h

**O que foi feito:**

- Realizamos a primeira reunião da equipe para discutir a proposta do projeto, alinhar as ideias iniciais e definir como seria o desenvolvimento do trabalho.
- Criamos e organizamos o repositório do projeto no GitHub e estruturamos o Diário de Bordo para registrar as atividades, evidências e horas de trabalho da equipe.
- **Felipe:** pesquisas para implementação de novas rotas, identificando que as tabelas de clima e tipo de veículo já existiam no banco de dados, mas ainda não eram utilizadas por nenhuma rota.

**Obstáculo:** Nenhum obstáculo relevante. A reunião foi utilizada principalmente para o planejamento inicial e a organização da equipe.

**Contato com o público:** Não houve contato com o público nesta semana. A atividade foi exclusivamente de planejamento e organização interna da equipe.

**Evidência coletada:** Registro da criação e organização do repositório no GitHub e do arquivo de Diário de Bordo, armazenados no próprio repositório da equipe.

**Próxima semana:** Definir com mais detalhes o escopo do projeto, dividir as primeiras tarefas entre os integrantes e iniciar a execução das atividades planejadas.

---

## Semana 2 — 25/09/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h; Felipe dos Reis Pena — 4h

**O que foi feito:**

- Upload dos instrumentos-modelo da disciplina para o repositório e revisão inicial da estrutura do diário de bordo para uso da equipe (commits `3ea102a` e `e6751ab`).
- Organização das branches e alinhamento inicial do fluxo de versionamento no GitHub.
- **Felipe:** pesquisas para implementação de novas rotas, sobre o uso dos marts já exportados.

**Obstáculo:** Dificuldade inicial em fechar qual recorte da plataforma principal de segurança viária seria exposto sem depender de todo o pipeline pesado de ETL.

**Contato com o público:** Não houve contato com o público externo nesta semana.

**Evidência coletada:** Commits `3ea102a` e `e6751ab` no histórico do repositório.

**Próxima semana:** Fechar o escopo enxuto da Trilha A (API pública de dados abertos) e publicar a estrutura inicial do serviço.

---

## Semana 3 — 02/10/2026

**Quem trabalhou e quanto:** Felipe dos Reis Pena — 4h

**O que foi feito:**

- **Felipe:** pesquisas para implementação de novas rotas. A rota `/api/v1/analises/perfil-rodovia`, que resultou dessa pesquisa, foi implementada em 13/10 e consta na semana 5.

**Obstáculo:** Sem registro nesta semana.

**Contato com o público:** Sem registro nesta semana.

**Evidência coletada:** Sem commit nesta semana; a primeira versão da rota está no commit `3a460a4` (13/10).

**Próxima semana:** Sem registro nesta semana.

---

## Semana 4 — 09/10/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Victor Cavalcante Pena — 4h; Felipe dos Reis Pena — 2h; Eduardo Rodrigues Bezerra Loiola — 1h; Jorge Leão Salgado Neto — 1h

**O que foi feito:**

- Redefinimos o escopo para uma API pública independente do dashboard, reutilizando a camada Gold da plataforma de segurança viária.
- Integramos o scaffold FastAPI ao repositório da disciplina (`app/main.py`, `app/routes.py`, `app/db.py`).
- Geramos um DuckDB compacto com `scripts/export_gold.py` e publicamos na release `data-2026-08-v1`.
- Executamos a suíte `pytest -q` e configuramos o GitHub Actions (`.github/workflows/ci.yml`).
- Revisamos `plano-de-acao.md`, `README.md` e distribuímos os papéis (Ayuri responsável por documentação, clareza do `/docs` e revisão do teste do estranho).
- Publicamos o endereço público no Render (`https://api-seguranca-viaria-ce.onrender.com`) e definimos perfis externos para os testes.
- **Felipe:** pesquisas para implementação de novas rotas, em especial sobre a análise de circunstâncias dos acidentes fatais (implementada em 13/10, semana 5).

**Obstáculo:** Entendimento inicial do fluxo de empacotamento do DuckDB para a nuvem gratuita sem acoplar o ETL completo da plataforma principal.

**Contato com o público:** Ainda não houve teste externo executado nesta semana; foi feita a preparação do roteiro em `docs/ROTEIRO-TESTE-EXTERNO.md`.

**Evidência coletada:** Commits `bf5ef69`, `aeb7509`, `dbe5e39`, `9b42f54`, `f39c0f3`, `4bbdf89` e tag `data-2026-08-v1`.

**Próxima semana:** Expandir as rotas analíticas, preparar formulário/convites para usuários externos e iniciar a coleta de logs de acesso.

---

## Semana 5 — 16/10/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h; Felipe dos Reis Pena — 4h; Eduardo Rodrigues Bezerra Loiola — 3h; Jorge Leão Salgado Neto — 2h

**O que foi feito:**

- Implementação e revisão das novas rotas de análise: `/api/v1/municipios/risco-per-capita`, `/api/v1/analises/circunstancias` e `/api/v1/analises/perfil-rodovia` (commits `54f61e7` a `a1c862c`), além de `/api/v1/analises/evolucao` e `/api/v1/analises/quando-acontece` (commit `eb03506`).
- Registro de acessos também na saída padrão (`ACESSO ...`) para leitura nos logs do Render (commit `256a6ca`).
- Criação de formulário de pesquisa técnica para avaliação por usuários externos e revisão da documentação das novas rotas no `README.md` (organização e revisão conduzidas com apoio de Ayuri).
- **Felipe:** implementação das rotas `/api/v1/municipios/risco-per-capita`, `/api/v1/analises/circunstancias` e `/api/v1/analises/perfil-rodovia`, com testes de erro e ordem estável das respostas (commit `3a460a4`, 13/10).

**Obstáculo:** O armazenamento local do Render gratuito é efêmero a cada reinício; por isso o middleware passou a gravar também linhas estruturadas `ACESSO` no stdout do serviço.

**Contato com o público:** Envio inicial do link público e abertura do formulário de feedback técnico (`https://docs.google.com/forms/d/e/1FAIpQLSd91nFu0ggNuwoBgZqxoXoMKLha7jGSmQ1hYihQPFp6WCMYfQ/viewform`).

**Evidência coletada:** Pull requests `#1` (`9654174`) e `#2` (`d00f52f`), commits na branch `dev-jorge` (`76e3c30`, `f8cb982`, `0dafe8f`, `fc2ef4f`) e primeiros registros em `evidencias/2026-11-12-logs-render.txt`.

**Próxima semana:** Aplicar o roteiro do "teste do estranho" sem orientação prévia e registrar as dificuldades reais de uso da documentação.

---

## Semana 6 — 23/10/2026

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

## Semana 7 — 30/10/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 2h; Felipe dos Reis Pena — 4h

**O que foi feito:**

- Acompanhamento da disponibilidade da URL pública (`https://api-seguranca-viaria-ce.onrender.com/health`) e verificação das consultas registradas nos endpoints de municípios, rodovias e trechos críticos.
- Revisão dos textos de limitações dos dados no `README.md` (recorte restrito a rodovias federais da PRF, instabilidade de taxas per capita em municípios pequenos e ano de 2026 parcial até 31/08/2026).
- **Felipe:** pesquisas para implementação de novas rotas, identificando oportunidades de utilização das tabelas de clima e tipo de veículo já existentes no banco de dados.

**Obstáculo:** Baixa adesão espontânea por formulário aberto sem convite individual; decidimos abordar diretamente perfis específicos do público-alvo (comunicação/jornalismo e desenvolvimento web) para observar o uso real.

**Contato com o público:** Convites diretos enviados para novos testadores externos avaliarem a URL pública.

**Evidência coletada:** Registros de acesso de 29/10 consolidados em `evidencias/2026-11-12-logs-render.txt`.

**Próxima semana:** Realizar segundo ciclo de teste externo e coletar feedback sobre uso prático dos dados.

---

## Semana 8 — 06/11/2026

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Jorge Leão Salgado Neto — 1h; Felipe dos Reis Pena — 4h

**O que foi feito:**

- Realização e registro do segundo teste com público externo em 06/11 (`evidencias/2026-11-06-teste-externo-02.md`), com estudante de comunicação/jornalismo interessado em dados de mobilidade.
- Mapeamento do obstáculo de *cold start* da instância gratuita do Render (cerca de 35 segundos na primeira requisição após inatividade) e dúvida sobre a comparação do ano parcial de 2026.
- **Felipe:** pesquisa para uma rota de condição do tempo, a partir da tabela de clima já exportada (implementada na semana 10).

**Obstáculo:** O tempo de despertar (*cold start*) do plano gratuito do Render fez a pessoa testadora achar inicialmente que o link estava fora do ar no primeiro clique.

**Contato com o público:** 2º teste externo documentado em 06/11 (formulário + conversa de acompanhamento).

**Evidência coletada:** `evidencias/2026-11-06-teste-externo-02.md` e linha correspondente em `evidencias.csv`.

**Próxima semana:** Preparar Marco 2, realizar terceiro teste externo e consolidar a contagem de acessos.

---

## Semana 9 — 13/11/2026

> Entrega do **Marco 2**.

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 3h; Felipe dos Reis Pena — 4h

**O que foi feito:**

- Condução do terceiro teste externo sem orientação em 12/11 com desenvolvedor web externo (`evidencias/2026-11-12-teste-externo-03.md`).
- Extração e consolidação das linhas de acesso da API com `scripts/summarize_access.py`, totalizando 41 consultas úteis bem-sucedidas (`evidencias/2026-11-12-logs-render.txt` e `evidencias/2026-11-12-resumo-acessos.md`).
- Conferência das rotas públicas no ar (`https://api-seguranca-viaria-ce.onrender.com/docs` e `/health`).
- **Felipe:** pesquisa para uma rota de tipos de veículo, a partir da tabela de veículos já exportada (implementada na semana 10).

**Obstáculo:** As atualizações documentais do Marco 2, a consolidação do `evidencias.csv` e o preenchimento do `marco-2.md` não haviam sido enviados para a branch `main` antes da verificação assíncrona do professor (que ocorreu sem encontro presencial na sexta-feira).

**Contato com o público:** 3º teste externo realizado em 12/11 com desenvolvedor web externo.

**Evidência coletada:** `evidencias/2026-11-12-teste-externo-03.md`, `evidencias/2026-11-12-logs-render.txt` e `evidencias/2026-11-12-resumo-acessos.md`.

**Próxima semana:** Incorporar devolutiva do Marco 2, subir todas as evidências, atualizar `/docs` com as melhorias pedidas pelos testadores e fechar a entrega do Marco 2 na `main`.

---

## Semana 10 — 20/11/2026

> Semana em andamento: o registro abaixo vai até 17/11 e será completado até o fim da semana.

**Quem trabalhou e quanto:** Ayuri de Souza dos Reis — 4h; Felipe dos Reis Pena — 4h

**O que foi feito:**

- Melhoria direta na clareza da documentação interativa `/docs` (`app/main.py` e `app/routes.py`), atendendo às dificuldades reais registradas nos testes externos: inclusão do guia **"Como começar sem ajuda"** no topo do Swagger, organização das rotas em `openapi_tags` (`meta`, `consultas`, `analises`) e adição de descrições e exemplos explícitos em todos os parâmetros (`ibge_code=2304400`, `rodovia` aceitando `116` ou `BR-116`, alerta de recorte parcial de `2026`).
- Adição de testes automatizados em `tests/test_api.py` para garantir que o schema `/openapi.json` mantenha as tags, instruções iniciais e descrições de parâmetros (`94 passed` na `main`).
- Preenchimento completo do `marco-2.md`, atualização do `evidencias.csv`, revisão do `docs/CHECKLIST-MARCO-2.md` e consolidação deste `diario-de-bordo.md` na branch `main`.
- **Felipe:** criação das rotas `/api/v1/analises/clima` e `/api/v1/analises/veiculos`, que passam a usar as tabelas de clima e de veículos já exportadas e antes sem rota (commit `bf4a8de`, 16/11), com os testes e as seções correspondentes no `README.md`.
- **Felipe:** criação da rota `/api/v1/analises/regioes` (17/11), que compara as regiões do Ceará (divisão do IBGE, em 6 regiões intermediárias ou 18 imediatas) por acidentes, mortes e feridos graves, em números absolutos e a cada 100 mil habitantes. Cada região traz também o município com mais acidentes. A rota aproveita as colunas de região da tabela municipal, que nenhuma rota usava até então, e aceita filtro por ano, escolha do nível, ordenação por seis indicadores e limite de resultados. Também foram escritos os testes automatizados da rota e a seção correspondente no `README.md`.

**Obstáculo:** Sincronização desigual de entregas entre integrantes da equipe; para não comprometer o registro do projeto e da etapa de documentação/experiência de uso, toda a frente de documentação, `/docs`, testes externos, evidências e ficha do Marco 2 foi consolidada e subida diretamente na `main`.

**Contato com o público:** Consolidação e anonimização por vínculo dos 3 testes externos em `evidencias/` e `evidencias.csv`.

**Evidência coletada:** `marco-2.md`, `evidencias.csv`, arquivos em `evidencias/` e commits de melhoria do `/docs` e da documentação na `main`.

**Próxima semana:** Fechar documentação final e preparar o Marco 3.

---

## Semana 11 — 27/11/2026

> Entrega do Marco 3. Registro parcial das atividades de 23/11/2026; complementar com resultados externos efetivamente obtidos até 27/11.

**Quem trabalhou e quanto:** Victor Cavalcante Pena — aproximadamente **5h em 23/11/2026** (2h já registradas na auditoria de evidências + cerca de 3h adicionais em interface, testes, documentação e preparação da avaliação externa, conforme estimativa do integrante). Registros dos demais integrantes pendentes de atualização individual.

**O que foi feito:**

- **Victor — auditoria:** implementação de `scripts/auditar_evidencias.py` e `tests/test_auditar_evidencias.py`; execução de 7 testes da auditoria, todos aprovados; verificação de 4 registros em `evidencias.csv` (0 erros estruturais e 3 alertas de comprovação).
- **Victor — interface:** implementação da página de consulta guiada `/explorar`, nos arquivos `app/explorer.py` e `app/static/explorar.html`, permitindo pesquisar dados por município e ano, consultar rankings de rodovias e examinar trechos de 10 km usando as rotas JSON já existentes.
- **Victor — acesso inicial:** alteração de `app/main.py` para redirecionar navegadores que solicitam HTML de `/` para `/explorar`, sem interromper a resposta JSON para clientes da API nem a documentação `/docs`.
- **Victor — qualidade:** inclusão de `tests/test_explorar.py` e verificação local de **137 testes automatizados aprovados**, com um aviso de depreciação não bloqueante; fluxos de CI do GitHub Actions concluídos com sucesso.
- **Victor — documentação:** criação de `docs/VALIDACAO-EXPLORAR.md` e atualização do `README.md` para destacar a interface pública, distinguir visitantes e desenvolvedores, explicar o acesso local e orientar a validação externa.
- **Victor — preparação de avaliação:** criação de um Google Forms de usabilidade com planilha vinculada e simplificação do questionário para 7 perguntas após retorno de que a versão inicial estava longa. A pesquisa busca registrar tarefas concluídas, facilidade de uso e sugestões, sem coletar nome ou e-mail no formulário.
- **Integração e publicação:** alterações da branch `dev-victor` revisadas no PR #5, integrado à `main` em 23/11/2026. Victor informou que o deploy público da interface no Render já foi realizado; registrar captura/verificação datada da URL pública como comprovação de disponibilidade.

**Obstáculos:** Os três testes externos anteriores têm registros textuais, mas ainda precisam de comprovação primária verificável. Embora o deploy no Render tenha sido informado como concluído, a equipe ainda deve guardar uma evidência técnica datada do funcionamento público. O questionário inicial recebeu crítica por ser longo, levando à sua redução.

**Contato com o público:** Em 23/11, Victor pediu a uma pessoa que conferisse a abertura do formulário; recebeu a observação de que ele estava muito longo, usada para simplificá-lo. **Esse retorno avalia o formulário, não constitui uma sessão concluída de teste da plataforma e não entra na contagem de participantes externos do Marco 3.**

**Evidência coletada:** PR #5 (`https://github.com/ayurireiscentraldedados/interface-grafica/pull/5`), commits e execução do GitHub Actions; código e testes de `/explorar`; documentação no repositório; formulário de avaliação (`https://docs.google.com/forms/d/e/1FAIpQLScYO5dqllE4L5dsXwMkozAsHMAAKx6R3SFJlDqfUKCRIJj8Kg/viewform`). Os links e o formulário **não substituem as respostas primárias de participantes**, que devem ser coletadas, preservadas em acesso restrito e anonimizadas antes da divulgação.

**Pendências antes de 27/11:** arquivar a comprovação do deploy público, realizar testes reais da interface, obter pelo menos 3 evidências primárias de pessoas externas, identificar e implementar pelo menos 2 melhorias comprovadamente motivadas por feedback externo e registrar as evidências em `evidencias.csv`.

**Próxima semana:** Preparar a socialização, consolidar os resultados do Marco 3 e finalizar a autoavaliação individual.

---

## Semana 12 — 04/12/2026

> **Socialização**.

**Quem trabalhou e quanto:** [PREENCHER NA SEMANA]

**O que foi feito:** [PREENCHER NA SEMANA]

**Obstáculo:** [PREENCHER NA SEMANA]

**Contato com o público:** [PREENCHER NA SEMANA]

**Evidência coletada:** [PREENCHER NA SEMANA]

**Próxima semana:** registrar o que fica publicado e encerrar a ação.
