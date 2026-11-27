# Marco 3 — 27/11/2026

## Identificação

- **Equipe:** Ayuri de Souza dos Reis; Victor Cavalcante Pena; Felipe dos Reis Pena; Eduardo Rodrigues Bezerra Loiola; Jorge Leão Salgado Neto.
- **Trilha:** A — API pública de dados abertos.
- **Produto:** [interface pública](https://api-seguranca-viaria-ce.onrender.com/explorar), [Swagger](https://api-seguranca-viaria-ce.onrender.com/docs) e [status](https://api-seguranca-viaria-ce.onrender.com/health).
- **Referência versionada:** base `1cb47241be784f9975182aa2876252d08ee05280`; a revisão final é o commit que contém este arquivo na branch de entrega (consultar histórico Git).

## Campo 1 — O que funciona hoje

A interface de consulta guiada e as rotas de API estão implementadas no repositório. O Marco 2 registrou resultados públicos de 299 acidentes em Fortaleza (2025) e os trechos BR-116 km 0–10 e km 10–20. Esses são resultados históricos documentados, não uma nova medição.

**Verificação HTTP da versão publicada antes da nova revisão:**
- `https://api-seguranca-viaria-ce.onrender.com/health`: não confirmado; ver JSON de evidência.
- `https://api-seguranca-viaria-ce.onrender.com/explorar`: não confirmado; ver JSON de evidência.
- `https://api-seguranca-viaria-ce.onrender.com/api/v1/municipios/2304400/indicadores?ano=2025`: não confirmado; ver JSON de evidência.
- `https://api-seguranca-viaria-ce.onrender.com/api/v1/rodovias?ano=2025&limit=3`: não confirmado; ver JSON de evidência.
- `https://api-seguranca-viaria-ce.onrender.com/api/v1/trechos-criticos?ano=2025&limit=3`: não confirmado; ver JSON de evidência.

Evidência técnica: [`evidencias/2026-11-27-verificacao-http.json`](evidencias/2026-11-27-verificacao-http.json). Testes locais da revisão: **139 testes aprovados nesta execução**. A publicação das alterações desta revisão deve ser confirmada após integração e deploy; os testes acima não comprovam o novo deploy.

## Campo 2 — O que mudou desde o Marco 2

- Interface `/explorar` para consultas sem código, redirecionamento HTML inicial, testes e protocolo de usabilidade (PR #5); PR #8 revisou a neutralidade do teste.
- Auditoria estrutural de evidências, com separação entre registros textuais e comprovantes primários.
- Consolidação de 12 respostas reais do Forms (23–24/11). Duas melhorias implementadas a partir de comentários registrados: busca por prefixo único (P08) e validação/obrigatoriedade contextual dos campos (P07). Reteste externo pendente.
- O questionário foi reduzido a sete perguntas após retorno sobre seu comprimento, conforme diário. Não se conta esse piloto como sessão de uso do produto.
- **Cortes:** nenhuma funcionalidade comprovadamente removida desde o Marco 2; a validação controlada por versão e a medição objetiva de todas as tarefas ficaram pendentes. Mantidas as restrições de dados e hospedagem já documentadas.

## Campo 3 — Alcance

| Indicador | Planejado | Obtido até hoje | Evidência |
| --- | ---: | --- | --- |
| Consultas úteis bem-sucedidas | ≥ 30 | 41 históricas entre 14/10 e 12/11; período posterior não apurado | `evidencias/2026-11-12-resumo-acessos.md` e logs associados |
| Pessoas externas testando | ≥ 3 | 12 respostas no Forms; independência e unicidade ainda não confirmadas | [`evidencias/2026-11-27-forms-usabilidade-anonimizado.csv`](evidencias/2026-11-27-forms-usabilidade-anonimizado.csv) |
| Mudanças motivadas pelo público | ≥ 2 | 2 alterações implementadas em código com vínculo explícito a comentários; reteste externo e confirmação de independência pendentes | `docs/FICHA-RESULTADOS-USABILIDADE.md`, `app/static/explorar.html` e histórico Git |

Facilidade média 8,17/10. Conclusão autodeclarada: 11/12 para município, rodovia e trecho; 10/12 para limitação. Não corresponde a taxa de acerto objetiva. Comentários autorizados: P08, “Tive que escrever o nome \"Fortaleza\" por completo”; P07 relatou ausência de aviso sobre obrigatoriedade de campos. A planilha original fica privada, com transcrição anonimizada no repositório. As 3 evidências textuais históricas do Marco 2 não foram convertidas retroativamente em prova primária.

## Campo 4 — Obstáculo e replanejamento

A devolutiva do Marco 2 exigiu comprovação de alcance além dos relatos escritos pela equipe. Priorizamos coleta real, anonimização e vínculo das melhorias com os comentários. O Forms anterior foi longo, e parte das respostas não contém valores concretos das tarefas. O recorte de versão por participante, identidade externa e duplicação não pôde ser confirmado apenas pelas respostas. Próximos passos: confirmar elegibilidade, retestar as duas correções com usuários independentes, verificar deploy da nova revisão, coletar logs recentes e preparar a socialização de 04/12.

## Campo 5 — Autopontuação proposta (a validar pela equipe)

| Dimensão | n.a.? | Pts (0–2) | Justificativa |
| --- | --- | ---: | --- |
| D1 Qualidade técnica | não | 1 | Interface/API implementadas; 139 testes aprovados nesta execução; ver evidências HTTP e confirmação de deploy pendente. |
| D2 Alcance e adequação ao público | não | 1 | Há respostas reais e melhorias vinculadas, mas não foi confirmada independência/retentativa. |
| D3 Documentação e reprodutibilidade | não | 2 | README, rotas, exemplos, dados, limitações e protocolo versionados. |
| D4 Registro do processo | não | 1 | Diário e evidências atualizados; horas/atribuições adicionais e comprovações antigas ainda incompletas. |
| D5 Autoavaliação e reflexão | não | 1 | Limitações e replanejamento explicitados; reflexões individuais ainda devem ser completadas. |

## Checklist final

- [x] Fonte, data, licença e limitações no README.
- [x] Rotas documentadas com exemplos e erros, observadas as limitações descritas.
- [ ] URL pública anterior confirmada por verificação técnica; conferir novo deploy.
- [x] Evidência quantitativa e qualitativa registradas (Forms anonimizado e logs históricos).
- [x] Diário complementado, sem inventar horas.
- [ ] Confirmar independência e unicidade de participantes, retestar melhorias e registrar versão.
- [ ] Finalizar autoavaliações individuais.
