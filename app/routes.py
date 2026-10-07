from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.db import (
    TABLES,
    columns,
    connect,
    quote_identifier,
    resolve_column,
    rows_as_dicts,
    table_exists,
)

router = APIRouter(prefix="/api/v1")

YEAR_COLS = ["year", "source_year", "ano"]
IBGE_COLS = ["ibge_code", "municipality_code", "codigo_ibge", "code_municipality"]
MUNICIPALITY_COLS = ["municipality", "municipality_name", "nome_municipio", "municipio"]
HIGHWAY_COLS = ["highway", "br", "road", "rodovia"]
ACCIDENTS_COLS = ["accidents", "accident_count", "total_accidents", "acidentes"]
DEATHS_COLS = ["deaths", "death_count", "total_deaths", "mortos", "mortes"]
SERIOUS_COLS = ["serious_injuries", "seriously_injured", "feridos_graves"]


def _ensure_table(conn, key: str) -> str:
    table = TABLES[key]
    if not table_exists(conn, table):
        raise HTTPException(
            status_code=503,
            detail=f"Dataset '{table}' não está disponível no banco exportado.",
        )
    return table


def _order_metric(conn, table: str) -> str | None:
    for candidates in (ACCIDENTS_COLS, DEATHS_COLS, SERIOUS_COLS):
        col = resolve_column(conn, table, candidates)
        if col:
            return col
    return None


@router.get("/datasets", summary="Lista os datasets publicados pela API")
def datasets() -> dict:
    conn = connect()
    try:
        result = []
        for key, table in TABLES.items():
            if table_exists(conn, table):
                result.append({"id": key, "table": table, "columns": columns(conn, table)})
        return {"count": len(result), "data": result}
    finally:
        conn.close()


@router.get("/municipios", summary="Lista municípios presentes na camada analítica")
def municipios(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 184,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "municipal")
        name_col = resolve_column(conn, table, MUNICIPALITY_COLS, required=True)
        code_col = resolve_column(conn, table, IBGE_COLS)
        year_col = resolve_column(conn, table, YEAR_COLS)

        selected = [f"{quote_identifier(name_col)} AS municipality"]
        if code_col:
            selected.insert(0, f"{quote_identifier(code_col)} AS ibge_code")

        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)

        sql = f"SELECT DISTINCT {', '.join(selected)} FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY municipality LIMIT ?"
        params.append(limit)

        data = rows_as_dicts(conn.execute(sql, params))
        return {"count": len(data), "filters": {"ano": ano}, "data": data}
    finally:
        conn.close()


@router.get(
    "/municipios/{ibge_code}/indicadores",
    summary="Retorna indicadores anuais de segurança viária de um município",
)
def indicadores_municipio(
    ibge_code: str,
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "municipal")
        code_col = resolve_column(conn, table, IBGE_COLS, required=True)
        year_col = resolve_column(conn, table, YEAR_COLS)

        where = [f"CAST({quote_identifier(code_col)} AS VARCHAR) = ?"]
        params: list[object] = [ibge_code]
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)

        sql = f"SELECT * FROM {quote_identifier(table)} WHERE {' AND '.join(where)}"
        if year_col:
            sql += f" ORDER BY {quote_identifier(year_col)}"

        data = rows_as_dicts(conn.execute(sql, params))
        if not data:
            raise HTTPException(status_code=404, detail="Município/ano não encontrado.")
        return {"count": len(data), "filters": {"ibge_code": ibge_code, "ano": ano}, "data": data}
    finally:
        conn.close()


@router.get("/rodovias", summary="Rankeia rodovias federais pelos indicadores observados")
def rodovias(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "highways")
        year_col = resolve_column(conn, table, YEAR_COLS)
        metric = _order_metric(conn, table)

        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)

        sql = f"SELECT * FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        if metric:
            sql += f" ORDER BY {quote_identifier(metric)} DESC"
        sql += " LIMIT ?"
        params.append(limit)

        data = rows_as_dicts(conn.execute(sql, params))
        return {"count": len(data), "filters": {"ano": ano, "limit": limit}, "data": data}
    finally:
        conn.close()


@router.get("/trechos-criticos", summary="Lista trechos de 10 km com maior concentração observada")
def trechos_criticos(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    rodovia: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "segments")
        year_col = resolve_column(conn, table, YEAR_COLS)
        highway_col = resolve_column(conn, table, HIGHWAY_COLS)
        metric = _order_metric(conn, table)

        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)
        if rodovia and highway_col:
            where.append(f"CAST({quote_identifier(highway_col)} AS VARCHAR) = ?")
            params.append(rodovia)

        sql = f"SELECT * FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        if metric:
            sql += f" ORDER BY {quote_identifier(metric)} DESC"
        sql += " LIMIT ?"
        params.append(limit)

        data = rows_as_dicts(conn.execute(sql, params))
        return {
            "count": len(data),
            "filters": {"ano": ano, "rodovia": rodovia, "limit": limit},
            "data": data,
        }
    finally:
        conn.close()


@router.get("/acidentes", summary="Consulta ocorrências georreferenciadas com filtros básicos")
def acidentes(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    municipio: str | None = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "accidents")
        year_col = resolve_column(conn, table, YEAR_COLS)
        municipality_col = resolve_column(conn, table, MUNICIPALITY_COLS)

        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)
        if municipio and municipality_col:
            where.append(f"LOWER({quote_identifier(municipality_col)}) = LOWER(?)")
            params.append(municipio)

        sql = f"SELECT * FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        data = rows_as_dicts(conn.execute(sql, params))
        return {
            "count": len(data),
            "filters": {"ano": ano, "municipio": municipio, "limit": limit, "offset": offset},
            "data": data,
        }
    finally:
        conn.close()
