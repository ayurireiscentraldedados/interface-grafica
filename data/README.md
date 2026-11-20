# Dados da API

Os dados reais **não são versionados** neste repositório.

O jeito mais fácil é baixar o banco já pronto (cerca de 3 MB) da release `data-2026-08-v1` e salvá-lo nesta pasta, como `data/ceara_road_safety_api.duckdb`:

```bash
curl -L -o data/ceara_road_safety_api.duckdb \
  https://github.com/ayurireiscentraldedados/interface-grafica/releases/download/data-2026-08-v1/ceara_road_safety_api.duckdb
```

No PowerShell do Windows, use `curl.exe` no lugar de `curl`. Rode o comando a partir da pasta raiz do projeto.

Se você tem a plataforma principal ao lado deste repositório, também pode gerar o arquivo a partir da camada Gold dela:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

O script copia apenas os marts usados pela API, mantendo este produto desacoplado do pipeline completo.
