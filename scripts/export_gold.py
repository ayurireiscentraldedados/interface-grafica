#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import duckdb

TABLES = [
    "dim_municipality",
    "mart_municipality_road_safety_yearly",
    "mart_highway_safety",
    "mart_highway_segment_safety",
    "mart_accident_map",
    "mart_weather_road_safety_pt",
    "mart_vehicle_road_safety",
]

REQUIRED = {
    "mart_municipality_road_safety_yearly",
    "mart_highway_safety",
    "mart_highway_segment_safety",
    "mart_accident_map",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta apenas os marts necessários da camada Gold para um DuckDB compacto da API."
    )
    parser.add_argument("--source", required=True, help="DuckDB da plataforma principal")
    parser.add_argument(
        "--output",
        default="data/ceara_road_safety_api.duckdb",
        help="Arquivo DuckDB de saída",
    )
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Fonte não encontrada: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    conn = duckdb.connect(str(output))
    source_sql = str(source).replace("'", "''")
    conn.execute(f"ATTACH '{source_sql}' AS source_db (READ_ONLY)")

    copied: list[str] = []
    missing: list[str] = []
    for table in TABLES:
        try:
            conn.execute(f'CREATE TABLE "{table}" AS SELECT * FROM source_db.gold."{table}"')
            copied.append(table)
            count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f"[ok] {table}: {count:,} linhas")
        except duckdb.Error:
            missing.append(table)
            print(f"[skip] {table}: não encontrado em source_db.gold")

    missing_required = sorted(REQUIRED.intersection(missing))
    if missing_required:
        conn.close()
        output.unlink(missing_ok=True)
        raise SystemExit(
            "Marts obrigatórios ausentes: " + ", ".join(missing_required) +
            ". Rode o dbt build da plataforma principal antes de exportar."
        )

    conn.execute("CREATE TABLE api_metadata (key VARCHAR PRIMARY KEY, value VARCHAR)")
    metadata = [
        ("generated_at_utc", datetime.now(timezone.utc).isoformat()),
        ("source_database", str(source)),
        ("copied_tables", ",".join(copied)),
    ]
    conn.executemany("INSERT INTO api_metadata VALUES (?, ?)", metadata)
    conn.close()
    print(f"\nBanco da API criado em: {output}")


if __name__ == "__main__":
    main()
