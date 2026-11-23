# Validação externa — Interface /explorar

**Objetivo:** verificar se uma pessoa externa ao projeto, sem familiaridade com APIs, consegue obter e interpretar os dados sem apoio da equipe.

## Antes de começar

- Conferir se a URL pública `/explorar` já está atualizada no Render. Se ainda não estiver, **não** iniciar o teste externo; aguardar o deploy.
- Explicar que a participação é voluntária e pedir autorização para guardar as respostas anonimizadas como evidência do projeto. Não publicar nomes, telefones, áudios, endereços de e-mail ou imagens de rosto.
- Enviar apenas a URL `https://api-seguranca-viaria-ce.onrender.com/explorar` e o enunciado abaixo, sem ensinar os passos.
- Registrar data, perfil aproximado da pessoa e versão/commit do serviço testado.

## Enunciado para a pessoa participante

> Estamos avaliando uma página de consulta a dados públicos. Sem pedir ajuda, tente: (1) descobrir o número de acidentes registrados em Fortaleza em 2025; (2) encontrar a rodovia federal com mais registros em 2025; (3) encontrar um trecho de 10 km entre os mais críticos; (4) dizer uma limitação que deve ser lembrada ao interpretar esses dados. Não tem problema errar: queremos descobrir o que precisamos melhorar.

## Ficha de sessão — preencher com fatos observados

- ID anônimo: P___
- Data e hora:
- Perfil geral (ex.: estudante de jornalismo):
- Dispositivo: celular / computador / outro
- Link e commit/versão testados:
- Consentimento para uso de respostas anonimizadas: sim / não
- Tempo total (min):
- Tarefa 1: concluiu sozinho / não concluiu — resposta e dificuldade:
- Tarefa 2: concluiu sozinho / não concluiu — resposta e dificuldade:
- Tarefa 3: concluiu sozinho / não concluiu — resposta e dificuldade:
- Tarefa 4: concluiu sozinho / não concluiu — resposta e dificuldade:
- O que mais confundiu? (resposta textual original):
- Qual melhoria faria? (resposta textual original):
- Facilidade de 0 a 10 (resposta original):
- Evidência primária guardada: exportação do Forms / captura autorizada / outro registro original
- Arquivo de comprovação anonimizado em `evidencias/`:

## Após a sessão

- Guardar exportação **original** das respostas e uma cópia anonimizada para o repositório, respeitando o consentimento. Não fabricar participantes nem preencher respostas por eles.
- Vincular a ficha e o comprovante a `evidencias.csv` sem contar o mesmo participante duas vezes.
- Registrar obstáculos e decisões de produto no diário **na semana em que ocorreram**.
- Registrar qualquer modificação efetivamente realizada e os testes posteriores. Não afirmar melhora sem medi-la.
- Se a API cair ou demorar a iniciar, registrar essa falha: ela é um resultado relevante do teste.
