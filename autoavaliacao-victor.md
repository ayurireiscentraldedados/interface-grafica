# Autoavaliação — Victor Cavalcante Pena

- **Nome:** Victor Cavalcante Pena
- **Equipe e trilha:** API Segurança Viária CE — Trilha A, API pública de dados abertos
- **Papel declarado no plano:** Backend e integração de dados

## Parte 1 — O que você fez

### 1. Seu papel mudou durante o semestre? Por quê?

Meu papel começou no backend e na integração dos dados da camada Gold com a API. Na reta final, passei a trabalhar também na interface, na qualidade e na validação com usuários. A API já oferecia consultas úteis, mas o Swagger exigia familiaridade com parâmetros técnicos. A interface `/explorar` foi uma forma de tornar o mesmo serviço utilizável por pessoas sem experiência com programação.

### 2. As três coisas mais substanciais que você produziu ou conduziu

1. Integração inicial do serviço FastAPI com os dados analíticos, incluindo a participação na preparação da camada Gold e na estruturação da API, conforme plano e diário da semana 4.
2. Implementação da interface `/explorar`, do redirecionamento inicial e dos testes associados, além da auditoria estrutural das evidências (`app/explorer.py`, `app/static/explorar.html`, `app/main.py`, `tests/test_explorar.py`, `scripts/auditar_evidencias.py` e PR #5).
3. Preparação do protocolo e do formulário de usabilidade, consolidação de 12 respostas anonimizadas, aplicação de duas correções relacionadas aos comentários e fechamento do Marco 3 (`docs/FICHA-RESULTADOS-USABILIDADE.md`, `evidencias/2026-11-27-forms-usabilidade-anonimizado.csv` e commit `cbbe7bc`). A suíte final passou com 139 testes.

### 3. Quanto tempo a ação consumiu por semana?

O diário registra 1h na semana de 18/09, 4h na semana de 09/10 e cerca de 5h em 23/11, totalizando aproximadamente 10h documentadas. Também houve trabalho de fechamento em 27/11, comprovado pelo commit `cbbe7bc`, mas sem duração aferida. Em relação às 28 horas de execução autônoma previstas, o registro disponível não comprova a carga integral. As horas restantes não podem ser estimadas retroativamente sem registro confiável.

## Parte 2 — O que aconteceu com a ação

| Indicador | Planejado | Obtido |
| :-- | :-- | :-- |
| consultas úteis bem-sucedidas | ≥ 30 | 41 históricas (14/10–12/11) |
| pessoas externas testando | ≥ 3 | 12 respostas; vínculo externo e unicidade a confirmar |
| mudanças motivadas pelo público | ≥ 2 | 2 alterações vinculadas a comentários; reteste externo pendente |

### Onde a diferença entre planejado e obtido foi maior?

Na qualidade da comprovação do alcance. O número de consultas documentadas superou a meta, e o formulário reuniu 12 respostas, mas nem todas incluem valores que permitam verificar o acerto das tarefas. A independência e unicidade dos respondentes também precisam ser confirmadas. Isso impede tratar a quantidade de respostas como quantidade comprovada de participantes externos.

### Alguém de fora usou o produto? Como você sabe?

Há três relatos externos históricos e 12 respostas do Forms em 23 e 24/11. O formulário traz avaliações, dificuldades e, em alguns casos, resultados encontrados. A evidência anonimizada está em `evidencias/2026-11-27-forms-usabilidade-anonimizado.csv`, com síntese em `docs/FICHA-RESULTADOS-USABILIDADE.md`. Esses registros demonstram respostas recebidas, mas ainda não confirmam por si só que todos eram pessoas externas e distintas. As verificações HTTP da equipe são evidência técnica, não alcance externo.

### O que o público disse que você não esperava ouvir?

Uma dificuldade interessante foi a necessidade de digitar o nome completo do município. Outra foi a falta de avisos sobre a obrigatoriedade dos campos. Eram detalhes que pareciam pequenos do ponto de vista técnico, mas afetavam a consulta. Por isso, a interface passou a aceitar prefixos únicos e a validar os campos de acordo com a aba selecionada. Ainda falta avaliar essas alterações com o público.

## Parte 3 — O que aconteceu com você

### O que você não sabia fazer em agosto e sabe agora?

O principal aprendizado que identifico neste projeto foi integrar a validação de usabilidade ao desenvolvimento de uma API de dados públicos: formular tarefas concretas, registrar evidências, separar testes automatizados de testes com pessoas e transformar comentários em melhorias rastreáveis. Não considero que ter construído a API, por si só, demonstre um aprendizado novo em ferramentas que eu já utilizava antes.

### Qual erro custou mais tempo? O que faria diferente?

Um problema concreto foi não consolidar continuamente as evidências e contribuições individuais. No Marco 2, parte dos registros só foi organizada depois da primeira avaliação. Na etapa seguinte foi necessário revisar evidências antigas, implementar uma auditoria e preparar um formulário mais curto. Eu organizaria desde o início commits pequenos, registro semanal das horas e coleta de evidência primária a cada teste, além de testar o próprio formulário antes de divulgá-lo.

### O que faltou para a ação sair melhor?

Faltou acompanhar com maior regularidade as horas, a utilização da API em produção e a validação com pessoas externas. Também seria importante ter separado os testes por versão e repetido as tarefas após as duas melhorias. A infraestrutura gratuita e a ausência de logs persistentes reforçam a necessidade de guardar evidências de forma periódica.

### A disciplina mudou algo sobre como você pensa dados públicos ou para quem programa?

A experiência reforçou que disponibilizar dados abertos não garante que eles sejam acessíveis ao público. A documentação técnica ajuda desenvolvedores, enquanto uma interface simples atende quem não conhece códigos IBGE ou Swagger. Também é importante explicar limitações do recorte, para não transformar contagens de acidentes em afirmações indevidas sobre risco.

## Parte 4 — A equipe

### Como o trabalho se distribuiu, honestamente?

Houve uma divisão inicial por backend, documentação, testes, infraestrutura e evidências. Minha atuação ficou concentrada na integração inicial e na reta final de interface, testes e validação. A equipe não manteve registros igualmente detalhados ao longo de todas as semanas, e a consolidação tardia dificultou acompanhar as contribuições individuais. Não atribuo horas ou tarefas que não estão demonstradas no diário ou no histórico.

### O que cada integrante fez que você não teria feito sozinho?

Ayuri contribuiu com documentação, organização e testes externos, incluindo as melhorias no Swagger. Felipe pesquisou e implementou rotas analíticas e os respectivos testes. Eduardo assumiu a frente de infraestrutura e publicação no plano; Jorge assumiu público externo e evidências. O diário registra atividades coletivas e contribuições de ambos na semana 5, mas nem todas são individualizadas, portanto não atribuo a eles entregas específicas além do que o registro permite. A divisão dessas frentes ajudou a manter o produto utilizável e documentado.

### Houve momento em que a equipe travou? Como saiu?

No Marco 2, houve dificuldade para sincronizar as entregas e demonstrar a participação e o alcance. A equipe consolidou o material na `main`, e a devolutiva do professor orientou uma revisão mais rigorosa da evidência externa. No Marco 3, contribuí com auditoria, interface, formulário e consolidação da entrega. Para o encerramento, ainda é necessário conferir o deploy e fazer a socialização com as limitações explicitadas.
