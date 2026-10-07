# Decisões de escopo

## Produto da disciplina

A equipe não irá reapresentar todo o Ceará Road Safety Data Platform como se tivesse sido construído na disciplina. O pipeline principal é tratado como **infraestrutura de dados preexistente**.

A contribuição específica desta ação é uma **API pública, documentada e reutilizável**, que transforma marts da camada Gold em um serviço simples para estudantes, pesquisadores, jornalistas de dados, desenvolvedores e pessoas interessadas em mobilidade.

## O que entra

- FastAPI e OpenAPI `/docs`;
- exportação compacta da camada Gold;
- consulta municipal;
- ranking de rodovias;
- trechos críticos de 10 km;
- consulta de acidentes georreferenciados;
- testes automatizados;
- documentação de fontes, limitações e licença;
- publicação da API;
- registro de uso e testes com público externo.

## O que fica fora

- reconstruir o ETL completo da PRF/IBGE/Open-Meteo;
- reproduzir o dashboard Streamlit dentro da API;
- autenticação de usuários;
- rotas de escrita/alteração de dados;
- inferência causal de risco;
- dados de acidentes fora da cobertura da PRF.

## Regra de honestidade acadêmica

Diário, evidências e marcos só devem afirmar atividades que de fato ocorreram. Arquivos futuros deste pacote estão marcados como planejados quando necessário e precisam ser atualizados pela equipe após a execução.
