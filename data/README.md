# Dados da API

Os dados reais **não são versionados** neste repositório.

Gere `data/ceara_road_safety_api.duckdb` a partir da camada Gold da plataforma principal:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

O script copia apenas os marts usados pela API, mantendo este produto desacoplado do pipeline completo.
