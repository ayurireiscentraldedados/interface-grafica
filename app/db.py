from __future__ import annotations

from typing import Iterable

import duckdb
from fastapi import HTTPException

from app.config import db_path


TABLES = {
    "municipal": "mart_municipality_road_safety_yearly",
    "highways": "mart_highway_safety",
    "segments": "mart_highway_segment_safety",
    "accidents": "mart_accident_map",
    "weather": "mart_weather_road_safety_pt",
    "vehicles": "mart_vehicle_road_safety",
    "municipalities": "dim_municipality",
}


def connect() -> duckdb.DuckDBPyConnection:
    path = db_path()
    if not path.exists():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Banco analítico não encontrado em '{path}'. "
                "Gere-o com scripts/export_gold.py ou configure ROAD_SAFETY_DB_PATH."
            ),
        )
    return duckdb.connect(str(path), read_only=True)


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


_COLUMNS_CACHE: dict[tuple[str, int, str], list[tuple[str, str]]] = {}


def _catalog(conn: duckdb.DuckDBPyConnection, table: str) -> list[tuple[str, str]]:
    # O banco é somente leitura; consultar o catálogo a cada busca de coluna custava mais da metade
    # do tempo de cada requisição. A chave inclui a data do arquivo, então trocar o banco renova o cache.
    path = db_path()
    try:
        stamp = path.stat().st_mtime_ns
    except OSError:
        stamp = 0
    key = (str(path), stamp, table)
    cached = _COLUMNS_CACHE.get(key)
    if cached is None:
        rows = conn.execute(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = ?
            ORDER BY ordinal_position
            """,
            [table],
        ).fetchall()
        cached = [(str(row[0]), str(row[1]).upper()) for row in rows]
        _COLUMNS_CACHE[key] = cached
    return cached


def columns(conn: duckdb.DuckDBPyConnection, table: str) -> list[str]:
    return [name for name, _ in _catalog(conn, table)]


def column_type(conn: duckdb.DuckDBPyConnection, table: str, column: str) -> str | None:
    for name, data_type in _catalog(conn, table):
        if name.lower() == column.lower():
            return data_type
    return None


def table_exists(conn: duckdb.DuckDBPyConnection, table: str) -> bool:
    return bool(columns(conn, table))


def resolve_column(
    conn: duckdb.DuckDBPyConnection,
    table: str,
    candidates: Iterable[str],
    *,
    required: bool = False,
) -> str | None:
    available = {c.lower(): c for c in columns(conn, table)}
    for candidate in candidates:
        if candidate.lower() in available:
            return available[candidate.lower()]
    if required:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "schema_incompativel",
                "table": table,
                "expected_one_of": list(candidates),
                "available_columns": sorted(available.values()),
            },
        )
    return None


def rows_as_dicts(cursor: duckdb.DuckDBPyConnection) -> list[dict]:
    description = cursor.description or []
    names = [item[0] for item in description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]
