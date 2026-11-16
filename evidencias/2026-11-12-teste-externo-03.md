# Registro de teste com público externo — 03

- **Data:** 2026-11-12
- **Vínculo da pessoa (anônimo):** Desenvolvedor web externo à instituição
- **Canal:** Conversa remota com envio da URL pública (`https://api-seguranca-viaria-ce.onrender.com`) e do `README.md`
- **Condução e registro:** Ayuri de Souza dos Reis (experiência de uso e validação pós-ajustes de documentação)

## Tarefas propostas (sem orientação prévia)

1. **Descobrir quais datasets a API oferece:** Concluída (`GET /api/v1/datasets`).
2. **Consultar os indicadores de um município em 2025:** Concluída de primeira usando `2304400` (Fortaleza) e `2312908` (Sobral) diretamente, guiado pelos exemplos do README.
3. **Encontrar as rodovias com maior número de acidentes em 2025:** Concluída via `GET /api/v1/rodovias?ano=2025&limit=5`.
4. **Encontrar os trechos críticos:** Concluída via `GET /api/v1/trechos-criticos?ano=2025&rodovia=116&limit=5`.
5. **Explicar uma limitação dos dados indicada no README:** Concluída; apontou que municípios pequenos apresentam taxas por 100 mil habitantes mais voláteis e que a causa registrada pela PRF é presumida.

## Respostas às perguntas pós-uso

- **Em qual etapa você travou?** Não travou nas rotas básicas; apenas notou que as rotas analíticas novas descritas no README ainda estavam marcadas como pendentes do próximo deploy na nuvem e precisavam ser testadas localmente até a atualização do serviço.
- **Algum nome de rota ou parâmetro ficou confuso?** Achou o padrão REST previsível (`ano`, `limit`, `offset`), sugerindo apenas manter todas as rotas agrupadas por categoria no Swagger (`/docs`).
- **O que você esperava encontrar e não encontrou?** Gostou de o cabeçalho CORS já vir liberado (`Access-Control-Allow-Origin: *`) para consumo direto no navegador.
- **Você usaria essa API em um trabalho, matéria, pesquisa ou aplicação? Para quê?** Sim, para alimentar um painel front-end ou mapa interativo sem precisar manter banco de dados próprio.
- **De 0 a 10, quão fácil foi começar sem ajuda?** Nota 9.

## Frase literal autorizada

> "A resposta em JSON já vem limpa e com CORS liberado para consumir direto no front-end, sem ter que baixar e tratar planilha da PRF."

## Alterações decididas pela equipe a partir do teste

1. Agrupar as rotas no `/docs` em seções claras (`meta`, `consultas` e `analises`) via `openapi_tags` no FastAPI.
2. Manter explícito no `README.md` e no `marco-2.md` o que já responde na URL pública do Render e o que está validado no repositório aguardando sincronização do deploy.
