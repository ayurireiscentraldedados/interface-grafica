# Resumo de consultas úteis à API — Marco 2

- **Data da consolidação:** 2026-11-12
- **Arquivo de origem:** `evidencias/2026-11-12-logs-render.txt`
- **Comando executado:**

```bash
python scripts/summarize_access.py --render-log evidencias/2026-11-12-logs-render.txt
```

## Saída consolidada

```text
Consultas úteis bem-sucedidas: 41
Período observado (UTC): 2026-10-14T13:16:05 até 2026-11-12T15:14:32
    6  /api/v1/municipios
    6  /api/v1/rodovias
    6  /api/v1/trechos-criticos
    5  /api/v1/datasets
    5  /api/v1/municipios/2304400/indicadores
    4  /api/v1/acidentes
    2  /api/v1/municipios/2312908/indicadores
    1  /api/v1/municipios/2303709/indicadores
    1  /api/v1/municipios/2307650/indicadores
    1  /api/v1/municipios/risco-per-capita
    1  /api/v1/analises/circunstancias
    1  /api/v1/analises/perfil-rodovia
    1  /api/v1/analises/evolucao
    1  /api/v1/analises/quando-acontece
```

## Observações

- O script ignora automaticamente chamadas às rotas de infraestrutura (`/`, `/health`, `/docs`, `/redoc` e `/openapi.json`) e contabiliza apenas requisições `GET` com status `2xx` sem duplicidade de timestamp.
- O registro preserva a privacidade dos usuários, armazenando apenas data/hora UTC, método, caminho, código HTTP e duração em milissegundos.
