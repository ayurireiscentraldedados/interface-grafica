# Registro de teste com público externo — 02

- **Data:** 2026-11-06
- **Vínculo da pessoa (anônimo):** Estudante de comunicação/jornalismo com interesse em dados públicos de mobilidade
- **Canal:** Formulário de pesquisa técnica (Google Forms) + conversa de acompanhamento
- **Condução e registro:** Jorge Leão Salgado Neto (formulário) e Ayuri de Souza dos Reis (consolidação das dificuldades de uso)

## Tarefas propostas (sem orientação prévia)

1. **Descobrir quais datasets a API oferece:** Concluída pelo navegador em `/docs` (`GET /api/v1/datasets`).
2. **Consultar os indicadores de um município em 2025:** Concluída utilizando o exemplo do README (`2304400` — Fortaleza, com 299 acidentes, 15 mortes e 71 feridos graves em 2025).
3. **Encontrar as rodovias com maior número de acidentes em 2025:** Concluída (`GET /api/v1/rodovias?ano=2025&limit=5`, identificando BR-116 com 707 acidentes e BR-222 com 359).
4. **Encontrar os trechos críticos:** Concluída (`GET /api/v1/trechos-criticos?ano=2025&limit=10`, identificando `BR-116 · km 0–10` com 138 acidentes, `BR-116 · km 10–20` com 97 e `BR-222 · km 0–10` com 60).
5. **Explicar uma limitação dos dados indicada no README:** Concluída; destacou que contagens brutas em rodovias mais movimentadas não representam risco por veículo sem dados de fluxo de tráfego e que 2026 só tem dados até agosto.

## Respostas às perguntas pós-uso

- **Em qual etapa você travou?** No primeiro acesso à URL pública: a página levou cerca de 35 segundos para abrir na primeira tentativa (hibernação da instância gratuita do Render), dando a impressão inicial de que o link estava fora do ar. Depois que carregou, as consultas responderam rápido.
- **Algum nome de rota ou parâmetro ficou confuso?** Questionou se consultar `ano=2026` nas rotas básicas já fazia ajuste proporcional ou se trazia apenas o acumulado até agosto.
- **O que você esperava encontrar e não encontrou?** Queria comparar rapidamente se 2026 estava pior ou melhor que 2025 no mesmo período e ver o ranking proporcional à população direto na documentação.
- **Você usaria essa API em um trabalho, matéria, pesquisa ou aplicação? Para quê?** Sim, para levantar rapidamente pautas sobre os trechos de 10 km com mais acidentes nas BRs do Ceará e cruzar com dados populacionais.
- **De 0 a 10, quão fácil foi começar sem ajuda?** Nota 9 (após o carregamento inicial do servidor).

## Frase literal autorizada

> "Ter os trechos de 10 km já somados por rodovia poupa horas de planilha para uma pauta, só achei que o link estava fora no primeiro clique porque demorou meio minuto para acordar."

## Alterações decididas pela equipe a partir do teste

1. Configurar monitoramento contínuo do endpoint `/health` a cada 5 minutos (UptimeRobot) e documentar no `README.md` o comportamento da hospedagem gratuita no Render.
2. Reforçar no `/docs` e no `README.md` o aviso sobre o recorte parcial de `2026` (observado até `31/08/2026` na release `data-2026-08-v1`) e o uso do parâmetro `comparar=mesmo_periodo` na rota `/api/v1/analises/evolucao`.
