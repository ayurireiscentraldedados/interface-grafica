# API de Disponibilização — Ceará Road Safety Data Platform

API destinada à **disponibilização de dados de segurança viária do estado do Ceará**, permitindo que outras aplicações, dashboards e análises consumam os dados produzidos pela plataforma.

O projeto integra dados públicos da **Polícia Rodoviária Federal (PRF)**, **IBGE** e **Open-Meteo**, realizando o tratamento, validação e organização dessas informações antes de sua disponibilização.

## Objetivo

O principal objetivo da API é servir como uma **camada de acesso aos dados de segurança viária**, facilitando o consumo das informações por sistemas externos.

Entre as informações disponíveis na plataforma estão:

- acidentes rodoviários;
- municípios;
- população;
- mortes;
- feridos;
- veículos envolvidos;
- características das rodovias;
- causas dos acidentes;
- tipos de acidentes;
- condições meteorológicas.

## Origem dos Dados

A API utiliza dados provenientes de diferentes fontes:

### PRF

Fornece os dados relacionados aos acidentes rodoviários, incluindo ocorrências, pessoas envolvidas, veículos, causas, tipos de acidentes, mortes, feridos e localização.

### IBGE

Fornece informações sobre os municípios e suas populações, permitindo relacionar os acidentes com os municípios do Ceará e gerar indicadores.

### Open-Meteo

Fornece informações meteorológicas utilizadas para complementar os registros de acidentes, considerando as condições climáticas próximas ao horário das ocorrências.

## Dados Disponibilizados

A API tem como base os modelos analíticos produzidos na camada **Gold** da plataforma.

Entre os principais modelos estão:

```text
dim_date
dim_municipality

fct_accident
fct_person_involvement
fct_municipality_population
fct_accident_weather

bridge_accident_cause
bridge_accident_type

mart_municipality_road_safety_yearly
mart_weather_road_safety
```

Esses modelos organizam os dados de forma adequada para consulta e utilização por sistemas que necessitam consumir informações sobre segurança viária.

## Principais Informações

### Acidentes

Informações sobre os acidentes registrados, incluindo data, município, localização, mortes, feridos, veículos e características da rodovia.

### Municípios

Dados dos municípios do Ceará e seus identificadores oficiais, permitindo relacionar os acidentes com a localização correspondente.

### População

Estimativas anuais da população dos municípios, utilizadas para complementar os dados de acidentes e gerar indicadores.

### Clima

Informações meteorológicas relacionadas às ocorrências, permitindo analisar a relação entre acidentes e condições climáticas.

### Causas e Tipos de Acidentes

Relacionamentos que permitem identificar as principais causas e os tipos de acidentes registrados.

## Indicadores

A camada analítica também permite disponibilizar informações agregadas por **município e ano**, como:

- quantidade de acidentes;
- número de mortes;
- número de feridos;
- população;
- indicadores de segurança viária.

Também são disponibilizados resultados relacionados às condições meteorológicas.

## Qualidade dos Dados

Os dados utilizados pela API passam por processos de tratamento e validação antes da disponibilização.

São verificados aspectos como:

- integridade dos registros;
- chaves dos municípios;
- dados populacionais;
- métricas não negativas;
- integridade referencial;
- cobertura dos dados meteorológicos;
- consistência das causas e tipos de acidentes.

Os testes de qualidade são realizados durante o processo de transformação dos dados.

## Tecnologias

- **Python** – processamento dos dados;
- **pandas** – manipulação de dados;
- **Apache Parquet** – armazenamento;
- **DuckDB** – processamento analítico;
- **dbt** – transformação e modelagem;
- **Docker** – ambiente da aplicação.

## Escopo Atual

O projeto utiliza dados da PRF referentes aos anos:

```text
2024
2025
2026
```

O ano de **2026 representa um período parcial** e não deve ser interpretado como um ano completo.

O projeto contempla os **184 municípios do Ceará** e disponibiliza dados organizados para análise de segurança viária.

## Utilização

A API pode ser utilizada como fonte de dados para:

- dashboards de segurança viária;
- aplicações web;
- sistemas de análise;
- estudos acadêmicos;
- relatórios e indicadores;
- outras aplicações que necessitem consumir os dados.
