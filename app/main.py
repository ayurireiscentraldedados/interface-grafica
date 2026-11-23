from __future__ import annotations

import csv
import logging
import time
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import access_log_path, db_path
from app.db import TABLES, connect, table_exists
from app.routes import router
from app.explorer import router as explorer_router

# O registro padrão do uvicorn escreve o IP e os parâmetros de cada consulta. A API usa só o registro abaixo.
logging.getLogger("uvicorn.access").disabled = True

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Verificação de disponibilidade (`/health`) e caminhos principais do serviço.",
    },
    {
        "name": "consultas",
        "description": (
            "Consultas diretas aos datasets e recortes de municípios, rodovias, trechos críticos (10 km) "
            "e ocorrências georreferenciadas."
        ),
    },
    {
        "name": "analises",
        "description": (
            "Análises agregadas prontas para uso: risco municipal por 100 mil habitantes, circunstâncias "
            "em acidentes fatais, perfil comparativo por rodovia, evolução temporal e distribuição por "
            "dia da semana e faixa horária."
        ),
    },
]

app = FastAPI(
    title="API Segurança Viária CE",
    version="0.1.0",
    description=(
        "API pública para consulta de indicadores e recortes de segurança viária em rodovias federais "
        "no Ceará (PRF, IBGE e Open-Meteo), construída a partir da camada Gold do Ceará Road Safety Data Platform.\n\n"
        "### Como começar sem ajuda\n"
        "1. Consulte `/api/v1/datasets` para ver as tabelas e colunas disponíveis no banco publicado.\n"
        "2. Consulte `/api/v1/municipios?ano=2025` para descobrir o `ibge_code` de qualquer município "
        "(ex.: Fortaleza = `2304400`, Sobral = `2312908`, Caucaia = `2303709`).\n"
        "3. Nos filtros de `rodovia`, você pode informar apenas o número (`116`) ou o prefixo (`BR-116`).\n"
        "4. **Atenção ao recorte temporal:** os anos de `2024` e `2025` estão completos; `2026` é parcial "
        "(observado até `31/08/2026` no pacote `data-2026-08-v1`)."
    ),
    openapi_tags=OPENAPI_TAGS,
    contact={
        "name": "Equipe API Segurança Viária CE — GitHub Issues",
        "url": "https://github.com/ayurireiscentraldedados/interface-grafica/issues",
    },
    license_info={"name": "MIT (código da equipe)", "url": "https://opensource.org/licenses/MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def access_log(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)

    # Deliberadamente não registra IP, nome, e-mail ou outro identificador pessoal.
    timestamp = datetime.now(timezone.utc).isoformat()
    path = access_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(["timestamp_utc", "method", "path", "status", "duration_ms"])
        writer.writerow([timestamp, request.method, request.url.path, response.status_code, duration_ms])

    # O disco gratuito do Render é apagado a cada reinício; esta linha vai também para os logs do serviço.
    print(f"ACESSO {timestamp} {request.method} {request.url.path} {response.status_code} {duration_ms}", flush=True)
    return response


@app.get("/", tags=["meta"])
def root() -> dict:
    return {
        "name": "API Segurança Viária CE",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1",
    }


@app.get("/health", tags=["meta"])
def health() -> dict:
    path = db_path()
    if not path.exists():
        return {
            "status": "degraded",
            "database": "missing",
            "path": str(path),
            "hint": "Execute scripts/export_gold.py para gerar o banco da API.",
        }

    conn = connect()
    try:
        available = [table for table in TABLES.values() if table_exists(conn, table)]
        return {
            "status": "ok",
            "database": "ready",
            "datasets_available": len(available),
            "datasets": available,
        }
    finally:
        conn.close()


app.include_router(router)
app.include_router(explorer_router)
