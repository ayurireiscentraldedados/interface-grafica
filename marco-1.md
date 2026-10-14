# Marco 1 — registro honesto do estado em 02/10

> Este arquivo foi preparado posteriormente a partir do material disponível no repositório. Ele **não deve afirmar que uma API pública já funcionava em 02/10 se isso não aconteceu**. Ajuste somente com fatos sustentados por commits/arquivos daquele período.

## Identificação

- **Equipe:** Ayuri de Souza dos Reis; Victor Cavalcante Pena; Felipe dos Reis Pena; Eduardo Rodrigues Bezerra Loiola; Jorge Leão Salgado Neto.
- **Marco e data:** Marco 1 — 02/10/2026.
- **Trilha:** A — API pública de dados abertos.
- **Endereço público do produto:** não havia endereço público confirmado no material recebido.
- **Commit desta entrega:** `e6751ab` (SHA completo `e6751aba1443fde733597f81bbdfdf753d0566fe`), de 25/09/2026. É o último commit do repositório até 02/10: não houve nenhum commit entre 25/09 e 04/10. Não existe tag desta data.

## Campo 1 — O que funcionava naquele momento

Com base apenas nos arquivos disponíveis:

1. O repositório da equipe existia no GitHub e continha só os modelos em branco da disciplina (pasta `03-modelos/`), com o diário de bordo já ajustado para a equipe.
2. O diário tinha a entrada da semana de 18/09: primeira reunião e criação do repositório.
3. Ainda não havia README do produto, código, nem a ideia da API escrita no repositório. O README entrou em 04/10 e o código da API em 07/10, os dois depois deste marco.

**Não há evidência suficiente no material recebido para afirmar que rotas HTTP estavam publicadas e utilizáveis por pessoa externa em 02/10.**

## Campo 2 — O que mudou desde o marco anterior

`n.a.`

## Campo 3 — Alcance

| Indicador | Planejado | Obtido até 02/10 | Onde está a evidência |
| :-- | :-- | :-- | :-- |
| consultas úteis à API | ainda não consolidado | 0 evidências registradas | `evidencias.csv` estava vazio |
| retorno externo | ainda não consolidado | 0 evidências registradas | `evidencias.csv` estava vazio |

**O que o público externo disse:** não há retorno externo registrado no material recebido.

## Campo 4 — Obstáculo e replanejamento

O principal risco observado é que, em 02/10, o repositório ainda não tinha o produto construído nem descrito, e a parte de uso externo, evidência e publicação não aparecia em nenhum arquivo. O replanejamento adotado é reduzir o escopo para uma API pública enxuta, reaproveitando a camada Gold já existente, e concentrar as próximas semanas em serviço funcional, documentação e público externo.

## Campo 5 — Autopontuação sugerida para discussão

> Ajustar em equipe; isto é uma sugestão conservadora, não uma nota oficial.

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | | 0 | não havia código da API no repositório em 02/10; a base técnica era a plataforma preexistente, que fica fora deste repositório |
| D2 Alcance e adequação ao público | sim | — | não havia contato externo registrado |
| D3 Documentação e reprodutibilidade | | 0 | não havia README do produto em 02/10; só os modelos em branco |
| D4 Registro do processo | | 1 | havia diário, porém somente uma semana aparece no material recebido |
| D5 Autoavaliação e reflexão | sim | — | dimensão ainda não aplicável no Marco 1 |

## Estado atual do repositório (acrescentado em 13/10/2026)

> Esta parte descreve o que existe **depois** do Marco 1. Ela não muda o que valia em 02/10, que está acima.

- **Último commit enviado:** `4bbdf89` (SHA completo `4bbdf8925ea00473a93eb64d1f656bb5e60f9959`), de 07/10/2026.
- **O que existe:** API FastAPI com as rotas de municípios, indicadores por município, rodovias, trechos críticos e acidentes; script que gera o banco compacto; testes automáticos; teste no GitHub a cada envio de código.
- **Publicação:** a API está no ar em https://api-seguranca-viaria-ce.onrender.com. Em 13/10 o `/health` respondeu `ok`, com 7 conjuntos de dados carregados. Os dados vêm da release `data-2026-08-v1` (2024 e 2025 completos, 2026 até 31/08).
- **Em andamento no computador, ainda sem commit:** três rotas de análise (ranking de municípios por habitante, circunstâncias dos acidentes fatais, perfil das rodovias), mais testes de erro, filtro de rodovia aceitando `116` ou `BR-116` e registro de acessos que também vai para os logs do Render.
- **Público externo:** nenhum contato registrado até agora. O `evidencias.csv` continua vazio.
