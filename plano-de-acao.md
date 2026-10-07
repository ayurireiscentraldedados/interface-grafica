# Plano de ação — API Segurança Viária CE

## Identificação

- **Equipe:** Ayuri de Souza dos Reis; Victor Cavalcante Pena; Felipe dos Reis Pena; Eduardo Rodrigues Bezerra Loiola; Jorge Leão Salgado Neto. **Matrículas:** [PREENCHER].
- **Trilha:** **A — API pública de dados abertos**.
- **Área temática da PREX:** **Tecnologia e Produção** (proposta da equipe; confirmar se o professor deseja outra classificação).
- **Por que essa área:** o produto transforma dados públicos já tratados em um serviço digital aberto e reutilizável por pessoas e sistemas externos.
- **Repositório:** https://github.com/ayurireiscentraldedados/interface-grafica.

## Campo 1 — O problema

Uma pessoa que queira analisar segurança viária no Ceará precisa localizar bases de fontes diferentes, entender formatos e chaves, tratar dados e relacionar acidentes, municípios, população e clima antes de conseguir responder perguntas simples; isso cria uma barreira para estudantes, pesquisadores, jornalistas e desenvolvedores que não querem reconstruir toda a preparação dos dados.

## Campo 2 — O público externo

- **Quem é:** estudantes, pesquisadores, jornalistas de dados, desenvolvedores e profissionais interessados em mobilidade/segurança viária que precisem consultar dados agregados ou recortes de acidentes no Ceará.
- **Duas ou três pessoas reais desse grupo:** **[PREENCHER APÓS CONVITE REAL — não inventar nomes]**.
- **Já falamos com alguma? Quando falaremos?** Ainda não há evidência de conversa externa registrada no material recebido. A equipe deve convidar pelo menos três pessoas até **16/10**, realizando o primeiro teste até **23/10**.
- **Como essa pessoa vai descobrir que o produto existe:** convite direto para testes, divulgação no LinkedIn/rede pessoal da equipe, link público do serviço e README compartilhável.

## Campo 3 — Trilha e produto

- **O que é, em uma frase que caiba num tuíte, e onde ficará publicado:** uma API pública que devolve indicadores municipais, rodovias, trechos críticos e ocorrências de segurança viária do Ceará já tratadas a partir de PRF, IBGE e Open-Meteo, com documentação interativa e URL pública.
- **O que NÃO faz parte:** reconstruir o pipeline completo da plataforma principal; dashboard visual; autenticação; escrita/edição de dados; previsão de acidentes; inferência causal; cobertura de acidentes fora da base da PRF.

## Campo 4 — Fontes de dados

### Fonte 1 — PRF

| | |
| :-- | :-- |
| **Nome e órgão** | Dados de acidentes — Polícia Rodoviária Federal (PRF) |
| **Endereço** | https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf |
| **Licença — e o que ela permite ao nosso produto** | A página institucional descreve os dados como abertos, sem restrições de licença/patente/mecanismos de controle, passíveis de uso, reuso e redistribuição. A API mantém a atribuição à PRF. |
| **Atualização — periodicidade declarada e data do dado mais recente** | A PRF declara atualização mensal da base BAT. A cópia da plataforma usada nesta ação contém 2024, 2025 e 2026, sendo 2026 parcial. Antes de cada marco, registrar no README a data efetivamente coberta pelo banco exportado. |
| **Dado pessoal? — se sim, granularidade e o que será agregado** | A API não publica identificadores pessoais. São utilizados atributos de ocorrência e agregações analíticas já preparadas pela plataforma. |

### Fonte 2 — IBGE

| | |
| :-- | :-- |
| **Nome e órgão** | Municípios e estimativas populacionais — Instituto Brasileiro de Geografia e Estatística (IBGE) |
| **Endereço** | https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html |
| **Licença — e o que ela permite ao nosso produto** | Dados publicados nos canais de dados abertos/estatísticos do IBGE. A equipe mantém atribuição explícita à fonte e não altera a autoria do dado original. |
| **Atualização — periodicidade declarada e data do dado mais recente** | Estimativas municipais são anuais. A edição 2026 tem referência em 01/07/2026. |
| **Dado pessoal? — se sim, granularidade e o que será agregado** | Não. A API trabalha com identificação municipal e população agregada. |

### Fonte 3 — Open-Meteo

| | |
| :-- | :-- |
| **Nome e órgão/provedor** | Historical Weather API — Open-Meteo |
| **Endereço** | https://open-meteo.com/en/docs/historical-weather-api |
| **Licença — e o que ela permite ao nosso produto** | Dados sob CC BY 4.0, com atribuição. O serviço gratuito é para uso não comercial e possui limites de chamadas. A ação é educacional/não comercial. |
| **Atualização — periodicidade declarada e data do dado mais recente** | O enriquecimento histórico acompanha as datas das ocorrências processadas. A data efetiva do recorte deve ser a mesma registrada para a plataforma exportada. |
| **Dado pessoal? — se sim, granularidade e o que será agregado** | Não. São condições meteorológicas por coordenada e horário de ocorrência. |

## Campo 5 — Papéis

> Divisão proposta para dar responsabilidade verificável a cada integrante. A equipe deve confirmar/ajustar os papéis no próximo encontro e registrar qualquer mudança no diário.

| Integrante | Papel | O que fica sob sua responsabilidade |
| :-- | :-- | :-- |
| **Victor Cavalcante Pena** | Backend e integração de dados | FastAPI, exportação da camada Gold, contrato das rotas e integração com DuckDB. |
| **Ayuri de Souza dos Reis** | Documentação e experiência de uso | README, clareza da documentação `/docs`, revisão do teste do estranho e registro das dificuldades de uso. |
| **Felipe dos Reis Pena** | Qualidade e testes | testes automatizados, casos de erro, validação das rotas e checklist técnico de cada marco. |
| **Eduardo Rodrigues Bezerra Loiola** | Infraestrutura e publicação | Docker, configuração de execução, publicação pública, disponibilidade do endpoint e registro técnico de acesso. |
| **Jorge Leão Salgado Neto** | Público externo e evidências | recrutamento de testadores, execução das conversas, organização de `evidencias.csv` e preparação dos resultados para socialização. |

## Campo 6 — Cronograma

| Data | O que estará pronto |
| :-- | :-- |
| **02/10 (Marco 1)** | Estado real disponível no material: repositório estruturado, diário iniciado e definição inicial da proposta de API; o serviço ainda não estava completo/publicado. |
| **13/11 (Marco 2)** | API funcionando ponta a ponta em endereço público, `/docs` utilizável sem ajuda, rotas principais testadas, pelo menos um teste com pessoa externa e primeiro registro quantitativo de uso. |
| **27/11 (Marco 3)** | API estável e documentada, fontes/licenças/limitações atualizadas, testes automatizados verdes, pelo menos três retornos externos registrados e `evidencias.csv` consolidado. |
| **04/12 (Socialização)** | demonstração pública ensaiada, resultados de alcance apresentados, limitações e falhas discutidas e plano de continuidade definido. |

### Execução entre 07/10 e o Marco 2

- **07–10/10:** integrar o scaffold da API ao repositório e validar exportação da camada Gold.
- **11–16/10:** publicar uma primeira URL acessível e convidar testadores externos.
- **17–23/10:** realizar o primeiro teste sem orientação e corrigir pontos de fricção.
- **24–31/10:** melhorar documentação, erros e estabilidade; iniciar contagem de uso.
- **01–07/11:** segundo ciclo de teste externo e ajustes.
- **08–12/11:** congelar versão do Marco 2, revisar README, evidências e diário.

### Dependências externas

- **Hospedagem pública:** depende de escolher e configurar um serviço acessível externamente. Se a opção principal falhar, usar outra hospedagem compatível com Docker/Python ou reduzir temporariamente o banco exportado, mantendo as mesmas rotas.
- **Público externo:** depende de resposta a convites. Mitigação: convidar mais pessoas do que o mínimo e usar também a divulgação já feita em rede profissional para recrutar voluntários.
- **Fontes públicas:** a API servirá uma cópia analítica já exportada; indisponibilidade temporária de PRF/IBGE/Open-Meteo não derruba o serviço já publicado.

## Campo 7 — Indicadores

| | Medida | Como será coletada | Valor que seria bom |
| :-- | :-- | :-- | :-- |
| **Contagem** | número de consultas úteis bem-sucedidas às rotas `/api/v1/*` no período publicado | `logs/access.csv` + `scripts/summarize_access.py`, excluindo health/docs; salvar captura/arquivo de resumo em `evidencias/` | **≥ 30 consultas úteis** até 27/11 |
| **Qualitativa** | retorno de pessoas externas que tentaram usar a API sem orientação | roteiro em `docs/ROTEIRO-TESTE-EXTERNO.md`; registrar vínculo, tarefa, dificuldade e fala autorizada sem nome completo | **≥ 3 pessoas externas**, com pelo menos 2 mudanças/documentações motivadas pelos testes |

## Antes de entregar: prova dos nove

- [x] O escopo foi reduzido à camada pública de acesso, sem reconstruir todo o pipeline.
- [x] O produto ainda ajuda alguém mesmo sem dashboard.
- [x] Problema e produto podem ser entendidos sem explicar a arquitetura interna.
- [ ] Primeira conversa com público externo marcada com data e vínculo real.
- [x] Os indicadores podem ser coletados pela própria equipe sem depender de relatório de terceiro.
