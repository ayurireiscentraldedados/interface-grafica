# Resumo de contribuições por integrante (apoio ao Diário de Bordo)

> O registro semanal oficial da disciplina (com horas, obstáculos, contato com o público e evidências por semana) está em [`diario-de-bordo.md`](./diario-de-bordo.md).

## Ayuri Reis (`Ayuri de Souza dos Reis`)

**Papel no plano de ação:** Documentação e experiência de uso (`README`, clareza da documentação `/docs`, revisão do teste do estranho e registro das dificuldades de uso).

**O que fez:**

- Estruturou inicialmente o repositório da equipe e o modelo do diário de bordo (`3ea102a`, `e6751ab`), cobrando e organizando as entregas do grupo no Git.
- Aprimorou a documentação interativa `/docs` no FastAPI (`app/main.py` e `app/routes.py`) a partir das dificuldades observadas nos testes sem orientação:
  - adicionou o guia **"Como começar sem ajuda"** direto na abertura do `/docs`;
  - organizou os endpoints nas categorias `meta`, `consultas` e `analises` (`openapi_tags`);
  - documentou todos os parâmetros com descrições e exemplos (`ibge_code` como `2304400` para Fortaleza, `rodovia` aceitando `116` ou `BR-116`, e explicação do recorte parcial de `2026` até `31/08/2026`);
  - criou testes automatizados em `tests/test_api.py` validando a documentação gerada em `/openapi.json`.
- Conduziu e documentou os testes de uso sem orientação ("teste do estranho") e a consolidação de acessos na pasta `evidencias/` (`2026-10-23-teste-externo-01.md`, `2026-11-06-teste-externo-02.md`, `2026-11-12-teste-externo-03.md`, `2026-11-12-logs-render.txt` e `2026-11-12-resumo-acessos.md`) e no `evidencias.csv`.
- Preencheu e consolidou a entrega do `marco-2.md`, o checklist operacional (`docs/CHECKLIST-MARCO-2.md`), o `README.md` e as entradas semanais do `diario-de-bordo.md`.

---

## Felipe

**O que fez:**

- Cobrou o grupo para entregarem as modificações.
- Criou a versão inicial deste resumo por integrante.
- Criou seis rotas novas de análise na API:

### 1. Risco per capita

**Rota:** `/api/v1/municipios/risco-per-capita`

Ranqueia os municípios por acidentes, mortes ou feridos graves **a cada 100 mil habitantes**. Assim cidades pequenas e grandes ficam comparáveis, e Fortaleza não lidera só por ser grande.

### 2. Circunstâncias dos acidentes

**Rota:** `/api/v1/analises/circunstancias`

Mostra quais circunstâncias aparecem mais nos acidentes fatais. Dá para olhar por causa presumida, tipo de acidente, condição da pista ou iluminação. Para cada categoria, traz:

- quantos acidentes houve;
- quantos foram fatais;
- a fatia dela no total de fatais.

### 3. Perfil por rodovia

**Rota:** `/api/v1/analises/perfil-rodovia`

Monta um perfil comparável de cada rodovia federal. Traz:

- acidentes;
- mortes;
- proporção de acidentes fatais;
- o que predomina em horário, clima e tipo de veículo;
- os trechos mais críticos.

### 4. Condições do tempo

**Rota:** `/api/v1/analises/clima`

Cruza os acidentes com a condição do tempo (dados do Open-Meteo): céu limpo, chuva, garoa, tempestade etc. Para cada condição, traz acidentes, mortes, feridos graves, a proporção de acidentes fatais e as médias de temperatura e precipitação (ponderadas pelo número de acidentes). Também resume os acidentes com e sem precipitação.

### 5. Tipos de veículo

**Rota:** `/api/v1/analises/veiculos`

Compara os tipos de veículo envolvidos nos acidentes (motocicleta, automóvel, bicicleta etc.). Traz veículos envolvidos, ocupantes, mortes, feridos, a fatia de cada tipo nas mortes, mortes e feridos graves a cada 100 veículos e a idade média dos veículos. Dá para ordenar por qualquer uma dessas medidas e ignorar tipos com poucos veículos.

### 6. Regiões do Ceará

**Rota:** `/api/v1/analises/regioes`

Compara as regiões do IBGE (6 intermediárias ou 18 imediatas) por acidentes, mortes e feridos graves, em números absolutos e a cada 100 mil habitantes. Mostra também o município com mais acidentes em cada região e permite filtrar por ano.

---

## Eduardo

**O que fez:** duas análises novas.

### Evolução no tempo

Mostra acidentes, mortes e feridos graves **por ano ou por mês**, com a variação em porcentagem. Dá para ver o Ceará todo, um município ou uma rodovia.

Como 2026 só vai até agosto, ele é comparado com janeiro a agosto de 2025, e não com o ano inteiro. Assim a comparação fica justa.

### Quando acontece

Uma tabela de **dia da semana por horário**, com os **5 momentos mais críticos**. Responde perguntas como "sexta à noite é pior?".

---

## Victor

**O que fez:**

- Deu a ideia do projeto.
- Fez o primeiro protótipo, o empacotamento do DuckDB na release `data-2026-08-v1` e a publicação inicial no Render.

---

## Jorge

**O que fez:**

- Elaborou o formulário de pesquisa técnica (Google Forms) para coleta de feedback externo e colaborou nos testes da API.
