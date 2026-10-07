from __future__ import annotations

from pathlib import Path
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


def table_exists(conn: duckdb.DuckDBPyConnection, table: str) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?",
        [table],
    ).fetchone()
    return bool(row and row[0])


def columns(conn: duckdb.DuckDBPyConnection, table: str) -> list[str]:
    if not table_exists(conn, table):
        return []
    rows = conn.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = ?
        ORDER BY ordinal_position
        """,
        [table],
    ).fetchall()
    return [str(row[0]) for row in rows]


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
