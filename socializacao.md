# Socialização — 04/12/2026

> Roteiro de preparação. Preencher os campos de resultado somente depois que houver evidência real.

## Roteiro

| | O que dizer | O nosso conteúdo |
| :-- | :-- | :-- |
| 1 | O problema, com a pessoa dentro dele | Quem quer usar dados de segurança viária precisa hoje preparar e relacionar múltiplas fontes antes de responder perguntas simples. |
| 2 | O que é o produto e onde está no ar | API Segurança Viária CE, com URL pública e documentação `/docs`. |
| 3 | Demonstração ao vivo, do ponto de vista de quem usa | abrir `/docs` → consultar município → consultar rodovias → consultar trechos críticos. |
| 4 | Quem de fora usou, e o que essa pessoa disse | [PREENCHER A PARTIR DO `evidencias.csv`]. |
| 5 | O que não deu certo, e o que aprendemos | discutir ao menos um obstáculo técnico e um aprendizado com público externo, sem maquiar falhas. |
| 6 | O que fica no ar depois de 11/12, e com quem falar | informar URL, repositório, licença e responsável/contato durável. |

## Roteiro da demonstração

1. Abrir a URL pública e mostrar que uma pessoa não precisa instalar nada para ler a documentação.
2. Abrir `/docs` e executar `GET /api/v1/municipios?ano=2025`.
3. Executar `GET /api/v1/municipios/2304400/indicadores?ano=2025` e explicar os campos retornados sem extrapolar o que os dados medem.
4. Executar `GET /api/v1/rodovias?ano=2025&limit=10`.
5. Executar `GET /api/v1/trechos-criticos?ano=2025&limit=10` e explicar que concentração histórica não é previsão de risco.
6. Mostrar rapidamente o README: fontes, licença e limitações.
7. Mostrar o resumo de alcance baseado em evidências reais.

**Plano B para queda de rede:** gravar até 02/12 uma demonstração curta e manter capturas sequenciais em `evidencias/`. Inserir aqui o caminho/link depois de produzido: **[PREENCHER]**.

## Convites

| Quem convidamos (vínculo) | Como convidamos | Data | Confirmou? |
| :-- | :-- | :-- | :-- |
| [pessoa externa 1] | [canal] | [data] | [ ] |
| [pessoa externa 2] | [canal] | [data] | [ ] |
| [pessoa externa 3] | [canal] | [data] | [ ] |

## Registro do público externo

| Nome ou vínculo | Como soube da ação | Contato, se autorizar |
| :-- | :-- | :-- |
| | | |
| | | |
| | | |
| | | |
| | | |

**Total de pessoas de fora presentes:** [PREENCHER]

## Depois da apresentação

- **A pergunta que não soubemos responder:** [PREENCHER NO MESMO DIA].
- **O que alguém de fora disse que não esperávamos ouvir:** [PREENCHER].
- **O que mudaríamos no produto por causa do que ouvimos hoje:** [PREENCHER].

## Antes do dia

- [ ] Convidamos ao menos uma pessoa de fora com antecedência.
- [ ] Demonstração ensaiada e cronometrada.
- [ ] Plano B gravado.
- [ ] Bloco sobre o que não deu certo mantido no roteiro.
- [ ] Folha de registro impressa.
- [ ] Autoavaliação de cada integrante pronta.
