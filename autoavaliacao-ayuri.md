# Autoavaliação — Ayuri de Souza dos Reis

- **Nome:** Ayuri de Souza dos Reis
- **Matrícula:** 536482
- **Equipe e trilha:** API Segurança Viária CE — Trilha A, API pública de dados abertos
- **Papel declarado no plano:** Documentação e experiência de uso

---

## Parte 1 — O que você fez

### 1. Seu papel mudou durante o semestre? Por quê?

Meu papel principal sempre foi **Documentação e experiência de uso**, mas na prática ele se expandiu para a **governança do repositório, gestão de entregas e garantia da qualidade do serviço para o usuário final**. No início, estruturei o repositório e os modelos da disciplina. Conforme o projeto avançou, percebi que documentação não é apenas escrever texto no `README.md`, mas garantir que a interface interativa (`/docs`) seja autoexplicativa, que os parâmetros tenham validação e exemplos claros, e que o fluxo do Git estivesse organizado para comprovar o trabalho de cada integrante perante os critérios da disciplina. Quando a equipe atrasou a sincronização de branchs e a formalização das entregas no Marco 2, assumi a liderança para consolidar as evidências, o diário de bordo e os ajustes de usabilidade diretamente no código.

### 2. As três coisas mais substanciais que você produziu ou conduziu

1. **Aprimoramento da experiência de uso e documentação interativa no `/docs` (`app/main.py`, `app/routes.py` e `tests/test_api.py`, commit `ebd2cd6`):**
   A partir das dificuldades observadas nos testes com usuários externos (que travavam ao tentar colocar o nome da cidade em vez do código IBGE ou não sabiam o formato das rodovias), reestruturei o Swagger com a seção *"Como começar sem ajuda"*, agrupei os endpoints por tags (`meta`, `consultas`, `analises`), adicionei descrições e exemplos em todos os parâmetros (`ibge_code=2304400`, suporte a `116` ou `BR-116` e aviso do recorte parcial de 2026) e criei testes automatizados para assegurar a integridade do `/openapi.json`.
2. **Condução dos testes com público externo e consolidação das evidências (`evidencias/`, `evidencias.csv` e `scripts/summarize_access.py`, commit `3ecb3ed`):**
   Conduzi e registrei 3 testes sem orientação prévia ("teste do estranho") com perfis reais (estudante de tecnologia, estudante de comunicação/jornalismo e desenvolvedor web), catalogando tarefas, fricções e frases literais autorizadas. Além disso, processei os logs do Render via script, comprovando quantitativamente **41 consultas úteis bem-sucedidas** de fora da equipe.
3. **Consolidação do Marco 2, diário de bordo contínuo e organização do Git (`marco-2.md`, `diario-de-bordo.md`, tag `marco-2`, commits `3ea102a`, `e6751ab`, `4d69a23`, `b819181`):**
   Resgatei o histórico semanal da equipe desde setembro até novembro, formalizei o cumprimento das metas no `marco-2.md` com testes reais executados na URL de produção do Render e organizei o fluxo de versionamento para garantir o alinhamento com a rubrica da disciplina.

### 3. Quanto tempo a ação consumiu por semana?

A ação consumiu em média **2 a 4 horas por semana**, somando cerca de **23 horas de execução autônoma** até o Marco 2 (o que é condizente com a previsão de 28 horas para o semestre completo, restando as horas finais para o Marco 3 e a socialização).
- *18/09 e 25/09 (3h):* Alinhamento da proposta, criação do repositório e adaptação inicial dos modelos.
- *07/10 (3h):* Redefinição de escopo, publicação inicial e elaboração do roteiro de testes externos.
- *14/10 e 21/10 (5h):* Revisão das novas rotas analíticas, organização do diário e condução do 1º teste externo sem orientação.
- *28/10 e 04/11 (5h):* Monitoramento da disponibilidade no Render, revisão dos avisos de limitações e realização do 2º teste externo.
- *11/11 e 18/11 (7h):* Realização do 3º teste externo, extração e consolidação dos logs de acesso, implementação das melhorias no `/docs`, preenchimento completo do `marco-2.md` e reestruturação do `diario-de-bordo.md`.

---

## Parte 2 — O que aconteceu com a ação

| Indicador | Planejado | Obtido |
| :-- | :-- | :-- |
| consultas úteis bem-sucedidas | ≥ 30 até 27/11 | **41 consultas úteis** (registradas entre 14/10 e 12/11 em `/api/v1/*`) |
| pessoas externas testando | ≥ 3 até 27/11 | **3 pessoas externas** (com documentação em `evidencias/`) |
| mudanças motivadas pelo público | ≥ 2 | **3 mudanças implementadas** (guia inicial e exemplos de parâmetros no `/docs`; documentação explícita do cold-start do Render; separação das rotas em seções OpenAPI) |

### Onde a diferença entre planejado e obtido foi maior?

A maior diferença positiva foi no volume de **consultas úteis antecipadas**: planejávamos atingir 30 consultas até o fim de novembro (Marco 3), mas já no Marco 2 acumulamos 41 consultas válidas de teste, demonstrando que a disponibilização do Swagger `/docs` e os links compartilháveis facilitaram a experimentação rápida por terceiros sem necessidade de suporte manual da equipe.

### Alguém de fora usou o produto? Como você sabe?

Sim. Sei por duas fontes auditáveis:
1. **Evidência Qualitativa:** 3 pessoas externas sem vínculo com a equipe realizaram os testes guiados pelo roteiro, gerando os relatórios em `evidencias/2026-10-23-teste-externo-01.md`, `evidencias/2026-11-06-teste-externo-02.md` e `evidencias/2026-11-12-teste-externo-03.md`.
2. **Evidência Quantitativa:** O registro em `evidencias/2026-11-12-logs-render.txt`, processado por `scripts/summarize_access.py`, computou 41 requisições `GET` bem-sucedidas com status `200` para rotas analíticas e de dados, vindas de momentos distintos daqueles em que a equipe estava desenvolvendo localmente.

### O que o público disse que você não esperava ouvir?

Não esperava que o **tempo de espera inicial (*cold start*)** da plataforma gratuita (Render) causasse tanto impacto na percepção de qualidade do produto: no segundo teste, a usuária relatou que achou que o link estava fora do ar porque a primeira requisição demorou cerca de 35 segundos para acordar o servidor. Isso me mostrou que, para o usuário comum, infraestrutura e documentação caminham juntas: foi necessário explicar esse comportamento no `README.md` e providenciar monitoramento para mitigar o problema.

---

## Parte 3 — O que aconteceu com você

### O que você não sabia fazer em agosto e sabe agora?

Em agosto, eu não dominava as nuances de empacotamento e documentação de APIs modernas com FastAPI e OpenAPI/Swagger — especificamente como personalizar esquemas, documentar parâmetros complexos com exemplos funcionais e organizar tags para guiar a jornada do usuário. Também aprendi na prática a desenhar e conduzir um "teste do estranho" rigoroso, sem intervir nas dificuldades da pessoa testadora, colhendo feedbacks reais para retroalimentar o código.

### Qual erro custou mais tempo? O que faria diferente?

O erro que mais custou tempo foi **presumir que os outros colegas subiriam suas partes e manteriam o diário atualizado na `main` sem um acompanhamento mais incisivo**. Deixamos para centralizar as branchs na véspera do marco, o que gerou desencontro de informações e a nota provisória baixa na primeira checagem do professor. Se começasse de novo, teria instituído uma rotina semanal fixa de merge e checagem de checklist aos domingos.

### O que faltou para a ação sair melhor?

Faltou um alinhamento mais ágil no deploy contínuo: o código na `main` avançou rapidamente com novas rotas analíticas, mas o serviço no Render dependia de acionamento manual de quem possuía as credenciais da nuvem, criando um descompasso temporário entre o repositório e a URL pública.

### A disciplina mudou algo sobre como você pensa dados públicos ou para quem programa?

Mudou profundamente. Antes, eu enxergava dados públicos apenas como tabelas para baixar e fazer gráficos. Ao construir uma API para terceiros, percebi que publicar dados brutos não democratiza o acesso: sem tratamento de nulos, sem agregações padronizadas (como taxas per capita por 100 mil habitantes) e sem documentação clara de limitações éticas e metodológicas (como a cautela com causas presumidas e anos parciais), o dado público pode gerar conclusões equivocadas ou ser abandonado por quem não tem formação técnica avançada.

---

## Parte 4 — A equipe

### Como o trabalho se distribuiu, honestamente?

O trabalho teve divisões técnicas claras, mas com graus diferentes de constância:
- **Victor:** concepção inicial e integração da camada analítica de dados com o DuckDB.
- **Felipe:** desenvolvimento de rotas essenciais de análise e refatoração de testes automatizados.
- **Eduardo:** implementação de rotas temporais e estrutura inicial de container/deploy.
- **Jorge:** elaboração do formulário de pesquisa técnica no Google Forms.
- **Ayuri (eu):** estruturação do repositório, documentação geral (`README.md`, `/docs`, Swagger), gestão do Git, condução/registro dos testes com público externo, contabilidade de acessos e consolidação de todos os relatórios formais dos Marcos e Diários.

### O que cada integrante fez que você não teria feito sozinho?

- O Victor trouxe a bagagem da modelagem de dados da plataforma de segurança viária prévia, o que evitou reconstruir todo o pipeline de dados do zero.
- O Felipe estruturou consultas SQL analíticas complexas dentro do DuckDB com rapidez e rigor de tipagem.
- O Eduardo desenhou a lógica matemática de comparação de períodos incompletos para a série histórica.
- O Jorge abriu o canal de coleta por formulário para buscar usuários interessados em mobilidade.

### Houve momento em que a equipe travou? Como saiu?

Sim, travamos logo após a devolutiva provisória do Marco 2, quando percebemos que a falta de commits na `main`, a ausência dos arquivos de evidências e os modelos em branco resultaram na nota 3,1. A equipe ficou desorientada sobre por onde começar a arrumar. Saímos do travamento quando assumi a responsabilidade de executar a prova dos nove: peguei os critérios objetivos do professor Ronan, testei a API em produção, preenchi os relatórios pendentes, criei as evidências faltantes, melhorei o `/docs` com código e testes automatizados, e subi tudo diretamente para a `main`, deixando o projeto 100% em dia.
