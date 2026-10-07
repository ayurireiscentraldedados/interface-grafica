from __future__ import annotations

import csv
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import access_log_path, db_path
from app.db import TABLES, connect, table_exists
from app.routes import router

app = FastAPI(
    title="API Segurança Viária CE",
    version="0.1.0",
    description=(
        "API pública para consulta de indicadores e recortes de segurança viária no Ceará, "
        "construída a partir da camada Gold do Ceará Road Safety Data Platform."
    ),
    license_info={"name": "MIT (código da equipe)"},
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
    path = access_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(["timestamp_utc", "method", "path", "status", "duration_ms"])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        ])
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
