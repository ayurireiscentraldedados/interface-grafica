# Diário de bordo

## Felipe

**O que fez:**

- Cobrou o grupo para entregarem as modificações
- Criou este diário de bordo.
- Criou três rotas novas de análise na API:

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
- Fez o primeiro protótipo.

---

## Ayuri

**O que fez:**

- Cobrou o grupo para entregarem as modificações.
- Conversou com o grupo.
- Organizou o git.
