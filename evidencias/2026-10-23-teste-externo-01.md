# Registro de teste com público externo — 01

- **Data:** 2026-10-23
- **Vínculo da pessoa (anônimo):** Estudante de graduação externo à turma (área de tecnologia/dados)
- **Canal:** Conversa síncrona com envio apenas da URL pública (`https://api-seguranca-viaria-ce.onrender.com/docs`) e do link do `README.md`
- **Condução e registro:** Ayuri de Souza dos Reis (revisão do teste do estranho e documentação)

## Tarefas propostas (sem orientação prévia)

1. **Descobrir quais datasets a API oferece:** Concluída sem dificuldade por meio da rota `GET /api/v1/datasets` no `/docs`.
2. **Consultar os indicadores de um município em 2025:** Concluída após uma tentativa inicial com erro. A pessoa tentou digitar `"Fortaleza"` diretamente no campo `ibge_code` de `GET /api/v1/municipios/{ibge_code}/indicadores` antes de notar que precisava consultar `GET /api/v1/municipios?ano=2025` para obter o código IBGE (`2304400`).
3. **Encontrar as rodovias com maior número de acidentes em 2025:** Concluída na primeira tentativa via `GET /api/v1/rodovias?ano=2025&limit=5` (identificou `BR-116` e `BR-222` no topo).
4. **Encontrar os trechos críticos:** Concluída via `GET /api/v1/trechos-criticos?ano=2025&limit=10`. Ficou em dúvida se o parâmetro `rodovia` aceitava `116` ou `BR-116`.
5. **Explicar uma limitação dos dados indicada no README:** Concluída; identificou que a base cobre apenas rodovias federais atendidas pela PRF (não inclui vias municipais ou estaduais) e que o ano de 2026 é parcial.

## Respostas às perguntas pós-uso

- **Em qual etapa você travou?** Na consulta de indicadores de um município específico, porque abriu o `/docs` direto sem ler o README e não sabia de cabeça o código IBGE de 7 dígitos.
- **Algum nome de rota ou parâmetro ficou confuso?** O parâmetro `ibge_code` precisava de um exemplo visível direto no Swagger (`/docs`), e o filtro `rodovia` não deixava claro na tela do `/docs` se devia usar `BR-116` ou só `116`.
- **O que você esperava encontrar e não encontrou?** Esperava ver no topo do `/docs` um resumo rápido de como começar sem precisar voltar ao GitHub.
- **Você usaria essa API em um trabalho, matéria, pesquisa ou aplicação? Para quê?** Sim, para trabalhos de análise exploratória e visualização de dados sem precisar limpar CSVs brutos da PRF.
- **De 0 a 10, quão fácil foi começar sem ajuda?** Nota 8.

## Frase literal autorizada

> "Pelo `/docs` deu para testar tudo direto no navegador sem instalar nada, mas na rota de indicadores por município tentei digitar o nome da cidade antes de ver que pedia o código do IBGE."

## Alterações decididas pela equipe a partir do teste

1. Adicionar no topo da documentação interativa (`/docs`, via `app/main.py`) a seção **"Como começar sem ajuda"**, já informando códigos IBGE de exemplo (`2304400` para Fortaleza, `2312908` para Sobral) e orientando a consultar `/api/v1/municipios`.
2. Documentar explicitamente nos parâmetros do FastAPI (`app/routes.py`) os exemplos de `ibge_code`, o suporte tanto a `116` quanto a `BR-116` no parâmetro `rodovia` e a organização das rotas em tags (`meta`, `consultas`, `analises`).
