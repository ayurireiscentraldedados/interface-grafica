from __future__ import annotations

import calendar
import re
from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query

from app.db import (
    TABLES,
    column_type,
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
ACCIDENT_KEY_COLS = ["accident_key", "accident_id", "id"]
ACCIDENTS_COLS = ["accidents", "accident_count", "total_accidents", "acidentes"]
DEATHS_COLS = ["deaths", "death_count", "total_deaths", "mortos", "mortes"]
SERIOUS_COLS = ["serious_injuries", "seriously_injured", "feridos_graves"]
POPULATION_COLS = ["population", "populacao", "estimated_population", "pop_estimate"]
ACCIDENT_TYPE_COLS = ["accident_type", "tipo_acidente", "type_accident"]
CAUSE_COLS = ["accident_cause", "cause", "causa_acidente", "causa_presumida", "probable_cause"]
ROAD_CONDITION_COLS = ["road_condition", "condicao_pista", "tipo_pista", "road_type", "tracado_via"]
LIGHTING_COLS = ["lighting", "iluminacao", "phase_of_day", "fase_dia", "day_phase"]
CLASSIFICATION_COLS = ["accident_classification", "classificacao_acidente", "classification"]
WEATHER_COLS = ["weather_condition", "weather", "condicao_metereologica", "condicao_meteorologica", "clima"]
VEHICLE_COLS = ["vehicle_type", "tipo_veiculo", "vehicle_category", "categoria_veiculo"]
HOUR_COLS = ["time_period", "period_of_day", "faixa_horaria", "hour_bucket", "hour", "hora"]
SEGMENT_START_COLS = ["segment_start_km", "start_km", "km_inicial", "km_inicio"]
SEGMENT_END_COLS = ["segment_end_km", "end_km", "km_final", "km_fim"]
DATE_COLS = ["event_timestamp", "accident_date", "data_inversa", "event_date", "date", "data"]
TIME_COLS = ["accident_time", "horario", "hora_inversa", "time", "hour", "hora"]
OBSERVED_THROUGH_COLS = ["observed_through_date"]
METRICS = ("acidentes", "mortes", "feridos_graves")
DAYS_OF_WEEK = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
SHIFTS = [("madrugada", 0, 5), ("manhã", 6, 11), ("tarde", 12, 17), ("noite", 18, 23)]
PROFILE_DIMENSIONS = {
    "horario": HOUR_COLS + LIGHTING_COLS,
    "clima": WEATHER_COLS,
    "tipo_veiculo": VEHICLE_COLS,
}
CIRCUMSTANCE_DIMENSIONS = {
    "tipo_acidente": ACCIDENT_TYPE_COLS,
    "causa": CAUSE_COLS,
    "condicao_pista": ROAD_CONDITION_COLS,
    "iluminacao": LIGHTING_COLS,
}


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


def _ranking_order(conn, table: str, metric: str | None) -> str:
    # Empates na métrica são comuns (70 de 100 trechos); sem desempate a mesma consulta pode
    # devolver linhas diferentes. Desempata por mortes, feridos graves e depois por identificadores.
    parts: list[str] = []

    def add(col: str | None, direction: str) -> None:
        item = f"{quote_identifier(col)} {direction}" if col else None
        if item and item not in parts:
            parts.append(item)

    add(metric, "DESC")
    for candidates in (ACCIDENTS_COLS, DEATHS_COLS, SERIOUS_COLS):
        add(resolve_column(conn, table, candidates), "DESC")
    for candidates in (HIGHWAY_COLS, SEGMENT_START_COLS, YEAR_COLS):
        add(resolve_column(conn, table, candidates), "ASC")
    return " ORDER BY " + ", ".join(parts) if parts else ""


def _stable_order(conn, table: str) -> str:
    key = resolve_column(conn, table, ACCIDENT_KEY_COLS)
    return f" ORDER BY {quote_identifier(key)}" if key else ""


def _fatal_expr(conn, table: str) -> str | None:
    deaths_col = resolve_column(conn, table, DEATHS_COLS)
    if deaths_col:
        return f"COALESCE(CAST({quote_identifier(deaths_col)} AS DOUBLE), 0) > 0"
    class_col = resolve_column(conn, table, CLASSIFICATION_COLS)
    if class_col:
        return f"LOWER(CAST({quote_identifier(class_col)} AS VARCHAR)) LIKE '%fata%'"
    return None


def _highway_variants(value: str) -> list[str]:
    text = value.strip()
    match = re.fullmatch(r"br[-\s]?(\d+)", text, flags=re.IGNORECASE)
    digits = match.group(1) if match else text if text.isdigit() else None
    if digits is None:
        return [text]
    return list(dict.fromkeys([text, f"BR-{digits}", digits]))


def _category_sql(col: str) -> str:
    return (
        f"COALESCE(NULLIF(TRIM(CAST({quote_identifier(col)} AS VARCHAR)), ''), "
        "'Não informado')"
    )


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
    "/municipios/risco-per-capita",
    summary="Rankeia municípios por acidentes, mortes e feridos graves por 100 mil habitantes",
)
def risco_per_capita(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    ordenar_por: Annotated[Literal["acidentes", "mortes", "feridos_graves"], Query()] = "acidentes",
    limit: Annotated[int, Query(ge=1, le=184)] = 20,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "municipal")
        name_col = resolve_column(conn, table, MUNICIPALITY_COLS, required=True)
        code_col = resolve_column(conn, table, IBGE_COLS)
        year_col = resolve_column(conn, table, YEAR_COLS)
        pop_col = resolve_column(conn, table, POPULATION_COLS)
        if pop_col is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Indicador per capita indisponível: a mart municipal publicada não contém "
                    f"coluna de população (aceitas: {', '.join(POPULATION_COLS)}). "
                    "Gere o banco novamente com scripts/export_gold.py a partir de uma camada "
                    "Gold que inclua população municipal."
                ),
            )

        metric_cols = {
            "accidents": resolve_column(conn, table, ACCIDENTS_COLS, required=True),
            "deaths": resolve_column(conn, table, DEATHS_COLS),
            "serious_injuries": resolve_column(conn, table, SERIOUS_COLS),
        }
        chosen_key = {
            "acidentes": "accidents",
            "mortes": "deaths",
            "feridos_graves": "serious_injuries",
        }[ordenar_por]
        if metric_cols[chosen_key] is None:
            raise HTTPException(
                status_code=503,
                detail=f"Indicador '{ordenar_por}' não está disponível nesta versão do banco exportado.",
            )

        pop = quote_identifier(pop_col)
        selected = []
        if code_col:
            selected.append(f"{quote_identifier(code_col)} AS ibge_code")
        selected.append(f"{quote_identifier(name_col)} AS municipality")
        if year_col:
            selected.append(f"{quote_identifier(year_col)} AS ano")
        selected.append(f"{pop} AS population")

        rate_exprs: dict[str, str] = {}
        for key, col in metric_cols.items():
            if col is None:
                continue
            rate_expr = (
                f"CASE WHEN {pop} IS NULL OR {pop} <= 0 THEN NULL "
                f"ELSE ROUND(CAST({quote_identifier(col)} AS DOUBLE) / {pop} * 100000, 2) END"
            )
            selected.append(f"{quote_identifier(col)} AS {key}")
            selected.append(f"{rate_expr} AS {key}_per_100k")
            rate_exprs[key] = rate_expr

        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)

        sql = f"SELECT {', '.join(selected)} FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += f" ORDER BY {rate_exprs[chosen_key]} DESC NULLS LAST, {quote_identifier(name_col)}"
        if year_col:
            sql += f", {quote_identifier(year_col)}"
        sql += " LIMIT ?"
        params.append(limit)

        data = rows_as_dicts(conn.execute(sql, params))
        return {
            "count": len(data),
            "filters": {"ano": ano, "ordenar_por": ordenar_por, "limit": limit},
            "data": data,
        }
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
        sql += _ranking_order(conn, table, metric)
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
            variants = _highway_variants(rodovia)
            where.append(
                f"UPPER(CAST({quote_identifier(highway_col)} AS VARCHAR)) "
                f"IN ({', '.join('UPPER(?)' for _ in variants)})"
            )
            params.extend(variants)

        sql = f"SELECT * FROM {quote_identifier(table)}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += _ranking_order(conn, table, metric)
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
        sql += _stable_order(conn, table) + " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        data = rows_as_dicts(conn.execute(sql, params))
        return {
            "count": len(data),
            "filters": {"ano": ano, "municipio": municipio, "limit": limit, "offset": offset},
            "data": data,
        }
    finally:
        conn.close()


@router.get(
    "/analises/circunstancias",
    summary="Circunstâncias registradas mais frequentes nos acidentes fatais",
)
def circunstancias(
    dimensao: Annotated[
        Literal["tipo_acidente", "causa", "condicao_pista", "iluminacao"], Query()
    ] = "causa",
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    municipio: str | None = None,
    ordenar_por: Annotated[Literal["fatais", "taxa_fatal"], Query()] = "fatais",
    min_acidentes: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "accidents")
        dim_col = resolve_column(conn, table, CIRCUMSTANCE_DIMENSIONS[dimensao])
        if dim_col is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Dimensão '{dimensao}' indisponível: a tabela de acidentes publicada não tem "
                    f"coluna correspondente (aceitas: {', '.join(CIRCUMSTANCE_DIMENSIONS[dimensao])})."
                ),
            )

        fatal_expr = _fatal_expr(conn, table)
        if fatal_expr is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Análise indisponível: a tabela de acidentes publicada não indica gravidade "
                    f"(aceitas: {', '.join(DEATHS_COLS + CLASSIFICATION_COLS)})."
                ),
            )

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

        sql = (
            f"SELECT {_category_sql(dim_col)} AS categoria, COUNT(*) AS acidentes, "
            f"SUM(CASE WHEN {fatal_expr} THEN 1 ELSE 0 END) AS acidentes_fatais "
            f"FROM {quote_identifier(table)}"
        )
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " GROUP BY 1"

        grouped = rows_as_dicts(conn.execute(sql, params))
        total_acidentes = sum(r["acidentes"] for r in grouped)
        total_fatais = sum(r["acidentes_fatais"] for r in grouped)

        items = [
            {
                "categoria": r["categoria"],
                "acidentes": r["acidentes"],
                "acidentes_fatais": r["acidentes_fatais"],
                "taxa_fatal_pct": round(100 * r["acidentes_fatais"] / r["acidentes"], 2),
                "pct_dos_acidentes_fatais": (
                    round(100 * r["acidentes_fatais"] / total_fatais, 2) if total_fatais else None
                ),
            }
            for r in grouped
            if r["acidentes"] >= min_acidentes
        ]
        sort_key = "acidentes_fatais" if ordenar_por == "fatais" else "taxa_fatal_pct"
        items.sort(key=lambda r: (-r[sort_key], -r["acidentes"], r["categoria"]))

        return {
            "count": min(len(items), limit),
            "filters": {
                "dimensao": dimensao,
                "ano": ano,
                "municipio": municipio,
                "ordenar_por": ordenar_por,
                "min_acidentes": min_acidentes,
                "limit": limit,
            },
            "total_acidentes": total_acidentes,
            "total_acidentes_fatais": total_fatais,
            "aviso": (
                "Frequência de uma circunstância entre acidentes registrados pela PRF em rodovias "
                "federais; não é risco nem causalidade. 'Causa' é a causa presumida registrada. "
                "Categorias com poucos acidentes têm taxas instáveis."
            ),
            "data": items[:limit],
        }
    finally:
        conn.close()


def _number(value):
    return int(value) if value is not None and float(value).is_integer() else value


def _map_profiles(conn, highways: list[str], ano: int | None) -> tuple[dict, list[str]]:
    profiles = {
        h: {"ocorrencias_mapeadas": 0, "pct_acidentes_fatais": None, "distribuicoes": {}}
        for h in highways
    }
    unavailable = list(PROFILE_DIMENSIONS)
    table = TABLES["accidents"]
    if not highways or not table_exists(conn, table):
        return profiles, unavailable
    hw_col = resolve_column(conn, table, HIGHWAY_COLS)
    if hw_col is None:
        return profiles, unavailable

    hw = f"CAST({quote_identifier(hw_col)} AS VARCHAR)"
    where = [f"{hw} IN ({', '.join('?' * len(highways))})"]
    params: list[object] = list(highways)
    year_col = resolve_column(conn, table, YEAR_COLS)
    if ano is not None and year_col:
        where.append(f"{quote_identifier(year_col)} = ?")
        params.append(ano)
    where_sql = " WHERE " + " AND ".join(where)

    fatal = _fatal_expr(conn, table)
    fatal_sql = f"SUM(CASE WHEN {fatal} THEN 1 ELSE 0 END)" if fatal else "NULL"
    sql = f"SELECT {hw}, COUNT(*), {fatal_sql} FROM {quote_identifier(table)}{where_sql} GROUP BY 1"
    for name, total, fatais in conn.execute(sql, params).fetchall():
        profiles[name]["ocorrencias_mapeadas"] = total
        if fatais is not None and total:
            profiles[name]["pct_acidentes_fatais"] = round(100 * fatais / total, 2)

    unavailable = []
    for dim, candidates in PROFILE_DIMENSIONS.items():
        col = resolve_column(conn, table, candidates)
        if col is None:
            unavailable.append(dim)
            continue
        sql = (
            f"SELECT {hw}, {_category_sql(col)} AS categoria, COUNT(*) "
            f"FROM {quote_identifier(table)}{where_sql} GROUP BY 1, 2"
        )
        grouped: dict[str, list[tuple[str, int]]] = {}
        for name, categoria, count in conn.execute(sql, params).fetchall():
            grouped.setdefault(name, []).append((categoria, count))
        for name, cats in grouped.items():
            cats.sort(key=lambda c: (-c[1], c[0]))
            total = sum(c[1] for c in cats)
            profiles[name]["distribuicoes"][dim] = [
                {"categoria": c, "acidentes": n, "pct": round(100 * n / total, 2)}
                for c, n in cats[:3]
            ]
    return profiles, unavailable


def _critical_segments(conn, highways: list[str], ano: int | None, n: int) -> dict[str, list[dict]]:
    table = TABLES["segments"]
    if n == 0 or not highways or not table_exists(conn, table):
        return {}
    hw_col = resolve_column(conn, table, HIGHWAY_COLS)
    start_col = resolve_column(conn, table, SEGMENT_START_COLS)
    end_col = resolve_column(conn, table, SEGMENT_END_COLS)
    acc_col = resolve_column(conn, table, ACCIDENTS_COLS)
    deaths_col = resolve_column(conn, table, DEATHS_COLS)
    if not (hw_col and start_col and end_col and acc_col):
        return {}

    where = [f"CAST({quote_identifier(hw_col)} AS VARCHAR) IN ({', '.join('?' * len(highways))})"]
    params: list[object] = list(highways)
    year_col = resolve_column(conn, table, YEAR_COLS)
    if ano is not None and year_col:
        where.append(f"{quote_identifier(year_col)} = ?")
        params.append(ano)
    deaths_sql = f"SUM({quote_identifier(deaths_col)})" if deaths_col else "NULL"
    sql = f"""
        SELECT rodovia, km_inicial, km_final, acidentes, mortes FROM (
            SELECT *, ROW_NUMBER() OVER (
                PARTITION BY rodovia ORDER BY acidentes DESC, mortes DESC NULLS LAST, km_inicial
            ) AS rn FROM (
                SELECT CAST({quote_identifier(hw_col)} AS VARCHAR) AS rodovia,
                       {quote_identifier(start_col)} AS km_inicial,
                       {quote_identifier(end_col)} AS km_final,
                       SUM({quote_identifier(acc_col)}) AS acidentes,
                       {deaths_sql} AS mortes
                FROM {quote_identifier(table)} WHERE {' AND '.join(where)} GROUP BY 1, 2, 3
            )
        ) WHERE rn <= ? ORDER BY rodovia, rn
    """
    result: dict[str, list[dict]] = {}
    for item in rows_as_dicts(conn.execute(sql, params + [n])):
        result.setdefault(item.pop("rodovia"), []).append({k: _number(v) for k, v in item.items()})
    return result


@router.get(
    "/analises/perfil-rodovia",
    summary="Perfil comparável de cada rodovia federal: indicadores, características e trechos críticos",
)
def perfil_rodovia(
    rodovia: str | None = None,
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    ordenar_por: Annotated[
        Literal["mortes", "acidentes", "mortes_por_100_acidentes"], Query()
    ] = "mortes",
    min_acidentes: Annotated[int, Query(ge=1)] = 1,
    trechos: Annotated[int, Query(ge=0, le=10)] = 3,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "highways")
        hw_col = resolve_column(conn, table, HIGHWAY_COLS, required=True)
        acc_col = resolve_column(conn, table, ACCIDENTS_COLS, required=True)
        deaths_col = resolve_column(conn, table, DEATHS_COLS)
        serious_col = resolve_column(conn, table, SERIOUS_COLS)
        year_col = resolve_column(conn, table, YEAR_COLS)
        if ordenar_por != "acidentes" and deaths_col is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Ordenação '{ordenar_por}' indisponível: a tabela de rodovias publicada não tem "
                    f"coluna de mortes (aceitas: {', '.join(DEATHS_COLS)})."
                ),
            )

        hw = f"CAST({quote_identifier(hw_col)} AS VARCHAR)"
        where = []
        params: list[object] = []
        if ano is not None and year_col:
            where.append(f"{quote_identifier(year_col)} = ?")
            params.append(ano)
        if rodovia:
            variants = _highway_variants(rodovia)
            where.append(f"UPPER({hw}) IN ({', '.join('UPPER(?)' for _ in variants)})")
            params.extend(variants)
        deaths_sql = f"SUM({quote_identifier(deaths_col)})" if deaths_col else "NULL"
        serious_sql = f"SUM({quote_identifier(serious_col)})" if serious_col else "NULL"
        sql = (
            f"SELECT {hw} AS rodovia, SUM({quote_identifier(acc_col)}) AS acidentes, "
            f"{deaths_sql} AS mortes, {serious_sql} AS feridos_graves "
            f"FROM {quote_identifier(table)}"
        )
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " GROUP BY 1"

        rows = rows_as_dicts(conn.execute(sql, params))
        if rodovia and not rows:
            raise HTTPException(status_code=404, detail="Rodovia/ano não encontrada.")

        profiles = []
        for r in rows:
            acidentes = _number(r["acidentes"])
            if acidentes is None or acidentes < min_acidentes:
                continue
            mortes = _number(r["mortes"])
            profiles.append(
                {
                    "rodovia": r["rodovia"],
                    "acidentes": acidentes,
                    "mortes": mortes,
                    "feridos_graves": _number(r["feridos_graves"]),
                    "mortes_por_100_acidentes": (
                        round(100 * mortes / acidentes, 2) if mortes is not None and acidentes else None
                    ),
                }
            )
        profiles.sort(key=lambda p: (-(p[ordenar_por] or 0), -p["acidentes"], p["rodovia"]))
        profiles = profiles[:limit]

        names = [p["rodovia"] for p in profiles]
        map_profiles, unavailable = _map_profiles(conn, names, ano)
        segments = _critical_segments(conn, names, ano, trechos)
        for position, p in enumerate(profiles, start=1):
            extra = map_profiles[p["rodovia"]]
            p["posicao"] = position
            p["ocorrencias_mapeadas"] = extra["ocorrencias_mapeadas"]
            p["pct_acidentes_fatais"] = extra["pct_acidentes_fatais"]
            p["predominantes"] = {d: v[0]["categoria"] for d, v in extra["distribuicoes"].items()}
            p["distribuicoes"] = extra["distribuicoes"]
            p["trechos_criticos"] = segments.get(p["rodovia"], [])

        return {
            "count": len(profiles),
            "filters": {
                "rodovia": rodovia,
                "ano": ano,
                "ordenar_por": ordenar_por,
                "min_acidentes": min_acidentes,
                "trechos": trechos,
                "limit": limit,
            },
            "dimensoes_indisponiveis": unavailable,
            "aviso": (
                "Indicadores observados em acidentes registrados pela PRF em rodovias federais; "
                "não medem risco por viagem nem por km rodado (não há denominador de tráfego) e "
                "não indicam causalidade. Distribuições e pct_acidentes_fatais vêm das ocorrências "
                "mapeadas e podem divergir dos totais da tabela de rodovias."
            ),
            "data": profiles,
        }
    finally:
        conn.close()


def _pct_change(new, base):
    if new is None or base is None or base == 0:
        return None
    return round(100 * (new - base) / base, 2)


def _scope_where(
    conn, table: str, ano: int | None, municipio: str | None, rodovia: str | None, year_sql: str | None = None
) -> tuple[list[str], list[object]]:
    where: list[str] = []
    params: list[object] = []
    if ano is not None:
        if year_sql is None:
            year_col = resolve_column(conn, table, YEAR_COLS)
            year_sql = quote_identifier(year_col) if year_col else None
        if year_sql:
            where.append(f"{year_sql} = ?")
            params.append(ano)
    if municipio:
        name_col = resolve_column(conn, table, MUNICIPALITY_COLS)
        if name_col:
            where.append(f"LOWER(CAST({quote_identifier(name_col)} AS VARCHAR)) = LOWER(?)")
            params.append(municipio)
    if rodovia:
        hw_col = resolve_column(conn, table, HIGHWAY_COLS)
        if hw_col:
            variants = _highway_variants(rodovia)
            where.append(
                f"UPPER(CAST({quote_identifier(hw_col)} AS VARCHAR)) "
                f"IN ({', '.join('UPPER(?)' for _ in variants)})"
            )
            params.extend(variants)
    return where, params


def _event_time(conn, table: str) -> tuple[str, str | None] | None:
    """Expressões SQL de data e de hora do evento; None quando a tabela não tem data."""
    date_col = resolve_column(conn, table, DATE_COLS)
    if date_col is None:
        return None
    date_sql = f"CAST({quote_identifier(date_col)} AS DATE)"
    hour_sql = None
    if (column_type(conn, table, date_col) or "").startswith("TIMESTAMP"):
        hour_sql = f"hour(CAST({quote_identifier(date_col)} AS TIMESTAMP))"
    else:
        time_col = resolve_column(conn, table, TIME_COLS)
        if time_col:
            hour_sql = f"hour(CAST({quote_identifier(time_col)} AS TIME))"
    return date_sql, hour_sql


def _map_metrics_sql(conn, table: str) -> dict[str, str]:
    deaths = resolve_column(conn, table, DEATHS_COLS)
    serious = resolve_column(conn, table, SERIOUS_COLS)
    return {
        "acidentes": "COUNT(*)",
        "mortes": f"COALESCE(SUM({quote_identifier(deaths)}), 0)" if deaths else "NULL",
        "feridos_graves": f"COALESCE(SUM({quote_identifier(serious)}), 0)" if serious else "NULL",
    }


def _data_window(conn) -> tuple[date | None, date | None]:
    """Primeira data com ocorrência e data até a qual a base foi observada (a base pode ter ano parcial)."""
    first = through = None
    accidents = TABLES["accidents"]
    if table_exists(conn, accidents):
        event = _event_time(conn, accidents)
        if event:
            first, through = conn.execute(
                f"SELECT MIN({event[0]}), MAX({event[0]}) FROM {quote_identifier(accidents)}"
            ).fetchone()
    municipal = TABLES["municipal"]
    if table_exists(conn, municipal):
        col = resolve_column(conn, municipal, OBSERVED_THROUGH_COLS)
        if col:
            value = conn.execute(
                f"SELECT MAX(CAST({quote_identifier(col)} AS DATE)) FROM {quote_identifier(municipal)}"
            ).fetchone()[0]
            through = value or through
    return first, through


def _months_between(first: date, last: date):
    year, month = first.year, first.month
    while (year, month) <= (last.year, last.month):
        yield year, month
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)


def _same_period_base(conn, scope, year: int, through: date) -> dict:
    # Mesmo intervalo do ano anterior (1º de janeiro até o mês/dia observado), nas ocorrências mapeadas.
    table = TABLES["accidents"]
    date_sql = _event_time(conn, table)[0]
    metrics = _map_metrics_sql(conn, table)
    where = [
        f"{date_sql} IS NOT NULL",
        f"year({date_sql}) = ?",
        f"month({date_sql}) * 100 + day({date_sql}) <= ?",
        *scope[0],
    ]
    params = [year, through.month * 100 + through.day, *scope[1]]
    sql = (
        f"SELECT {', '.join(f'{expr} AS {key}' for key, expr in metrics.items())} "
        f"FROM {quote_identifier(table)} WHERE {' AND '.join(where)}"
    )
    row = rows_as_dicts(conn.execute(sql, params))[0]
    return {k: _number(v) for k, v in row.items()}


@router.get(
    "/analises/evolucao",
    summary="Série anual ou mensal de acidentes, mortes e feridos graves, com variação percentual",
)
def evolucao(
    granularidade: Annotated[Literal["ano", "mes"], Query()] = "ano",
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    municipio: str | None = None,
    rodovia: str | None = None,
    comparar: Annotated[Literal["mesmo_periodo", "total"], Query()] = "mesmo_periodo",
) -> dict:
    conn = connect()
    try:
        accidents = TABLES["accidents"]
        use_map = granularidade == "mes" or bool(municipio and rodovia)
        event = None
        if table_exists(conn, accidents):
            event = _event_time(conn, accidents)
        if use_map:
            _ensure_table(conn, "accidents")
            if event is None:
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "Série mensal indisponível: a tabela de acidentes publicada não tem data da ocorrência "
                        f"(aceitas: {', '.join(DATE_COLS)})."
                    ),
                )
        map_scope = (
            _scope_where(conn, accidents, None, municipio, rodovia, f"year({event[0]})") if event else ([], [])
        )

        if use_map:
            date_sql = event[0]
            metrics = _map_metrics_sql(conn, accidents)
            select = [f"year({date_sql}) AS ano"]
            if granularidade == "mes":
                select.append(f"month({date_sql}) AS mes")
            select += [f"{expr} AS {key}" for key, expr in metrics.items()]
            group = ", ".join(str(i + 1) for i in range(len(select) - len(metrics)))
            sql = (
                f"SELECT {', '.join(select)} FROM {quote_identifier(accidents)} "
                f"WHERE {' AND '.join([f'{date_sql} IS NOT NULL', *map_scope[0]])} "
                f"GROUP BY {group} ORDER BY {group}"
            )
            params = list(map_scope[1])
            fonte = "ocorrências mapeadas"
            zero = {k: (None if expr == "NULL" else 0) for k, expr in metrics.items()}
        else:
            table = _ensure_table(conn, "highways" if rodovia else "municipal")
            year_col = resolve_column(conn, table, YEAR_COLS, required=True)
            acc_col = resolve_column(conn, table, ACCIDENTS_COLS, required=True)
            deaths_col = resolve_column(conn, table, DEATHS_COLS)
            serious_col = resolve_column(conn, table, SERIOUS_COLS)
            if rodovia:
                resolve_column(conn, table, HIGHWAY_COLS, required=True)
            else:
                resolve_column(conn, table, MUNICIPALITY_COLS, required=bool(municipio))
            where, params = _scope_where(conn, table, None, municipio, rodovia)
            year = quote_identifier(year_col)
            sql = (
                f"SELECT {year} AS ano, SUM({quote_identifier(acc_col)}) AS acidentes, "
                f"{f'SUM({quote_identifier(deaths_col)})' if deaths_col else 'NULL'} AS mortes, "
                f"{f'SUM({quote_identifier(serious_col)})' if serious_col else 'NULL'} AS feridos_graves "
                f"FROM {quote_identifier(table)}"
                f"{' WHERE ' + ' AND '.join(where) if where else ''} GROUP BY 1 ORDER BY 1"
            )
            fonte = "mart anual"

        rows = [
            {k: (_number(v) if k in METRICS else v) for k, v in r.items()}
            for r in rows_as_dicts(conn.execute(sql, params))
        ]
        if not rows and (municipio or rodovia):
            raise HTTPException(status_code=404, detail="Município/rodovia não encontrado.")

        first, through = _data_window(conn)
        partial_from = through if through and (through.month, through.day) != (12, 31) else None
        aviso = (
            "Variação percentual de acidentes registrados pela PRF em rodovias federais; não mede risco "
            "nem causalidade. Ano parcial é comparado com o mesmo intervalo do ano anterior "
            "(comparar=mesmo_periodo), para não parecer queda. Séries mensais e comparações por intervalo "
            "usam as ocorrências mapeadas, que podem divergir dos totais da mart anual. A variação é null "
            "quando o período-base é zero ou ausente; recortes pequenos têm variações instáveis."
        )
        if through is None:
            aviso += " A data até a qual a base foi observada não está disponível; o ano parcial não pôde ser identificado."

        data: list[dict] = []
        if granularidade == "mes":
            # Meses sem ocorrência são zeros de verdade; preenche a janela inteira para que
            # "mês anterior" e "mesmo mês do ano anterior" nunca apontem para um mês que só falta na lista.
            by_month = {(r["ano"], r["mes"]): r for r in rows}
            months = list(_months_between(first, through)) if rows else []

            def month_values(y: int, m: int) -> dict | None:
                if not months or not months[0] <= (y, m) <= months[-1]:
                    return None
                return by_month.get((y, m), zero)

            for y, m in months:
                if ano is not None and y != ano:
                    continue
                current = month_values(y, m)
                prev = month_values(y if m > 1 else y - 1, m - 1 if m > 1 else 12)
                same = month_values(y - 1, m)
                is_partial = bool(partial_from and (y, m) == (through.year, through.month)
                                  and through.day < calendar.monthrange(y, m)[1])
                data.append(
                    {
                        "periodo": f"{y}-{m:02d}",
                        "ano": y,
                        "mes": m,
                        **{k: current[k] for k in METRICS},
                        "parcial": is_partial,
                        **{f"var_pct_{k}": _pct_change(current[k], prev[k]) if prev else None for k in METRICS},
                        "var_pct_mesmo_mes_ano_anterior": {
                            k: _pct_change(current[k], same[k]) if same else None for k in METRICS
                        },
                        "base_comparacao": "mês anterior; mesmo mês do ano anterior",
                    }
                )
        else:
            by_year = {r["ano"]: r for r in rows}
            for r in rows:
                y = r["ano"]
                prev = by_year.get(y - 1)
                is_partial = None if through is None else bool(partial_from and y == through.year)
                base = prev
                label = f"ano {y - 1} inteiro" if prev else None
                if is_partial and comparar == "mesmo_periodo":
                    base, label = None, None
                    if event and prev:
                        base = _same_period_base(conn, map_scope, y - 1, through)
                        label = f"{y - 1}, de 1º de janeiro até {through.day:02d}/{through.month:02d}"
                data.append(
                    {
                        "periodo": y,
                        "ano": y,
                        **{k: r[k] for k in METRICS},
                        "parcial": is_partial,
                        **{f"var_pct_{k}": _pct_change(r[k], base[k]) if base else None for k in METRICS},
                        "base_comparacao": label,
                    }
                )
            if ano is not None:
                data = [item for item in data if item["ano"] == ano]
        if ano is not None and not data:
            raise HTTPException(status_code=404, detail="Ano não encontrado para o recorte pedido.")

        return {
            "count": len(data),
            "filters": {
                "granularidade": granularidade,
                "ano": ano,
                "municipio": municipio,
                "rodovia": rodovia,
                "comparar": comparar,
            },
            "fonte": fonte,
            "periodo_parcial": (
                {"ano": partial_from.year, "ate": partial_from.isoformat()} if partial_from else None
            ),
            "aviso": aviso,
            "data": data,
        }
    finally:
        conn.close()


@router.get(
    "/analises/quando-acontece",
    summary="Acidentes e mortes por dia da semana e faixa horária (mapa de calor)",
)
def quando_acontece(
    ano: Annotated[int | None, Query(ge=2007, le=2100)] = None,
    municipio: str | None = None,
    rodovia: str | None = None,
    faixa: Annotated[Literal["turno", "hora"], Query()] = "turno",
    min_acidentes: Annotated[int, Query(ge=1)] = 1,
) -> dict:
    conn = connect()
    try:
        table = _ensure_table(conn, "accidents")
        event = _event_time(conn, table)
        if event is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Análise indisponível: a tabela de acidentes publicada não tem data da ocorrência "
                    f"(aceitas: {', '.join(DATE_COLS)})."
                ),
            )
        date_sql, hour_sql = event
        metrics = _map_metrics_sql(conn, table)
        fatal = _fatal_expr(conn, table)
        fatal_sql = f"SUM(CASE WHEN {fatal} THEN 1 ELSE 0 END)" if fatal else "NULL"

        where, params = _scope_where(conn, table, ano, municipio, rodovia, f"year({date_sql})")
        in_scope = quote_identifier(table) + (" WHERE " + " AND ".join(where) if where else "")
        total_scope = conn.execute(f"SELECT COUNT(*) FROM {in_scope}", params).fetchone()[0]
        if total_scope == 0 and (ano is not None or municipio or rodovia):
            raise HTTPException(status_code=404, detail="Município/rodovia/ano não encontrado.")

        valid = [f"{date_sql} IS NOT NULL"] + ([f"{hour_sql} IS NOT NULL"] if hour_sql else [])
        sql = (
            f"SELECT isodow({date_sql}) AS dia, {hour_sql or 'NULL'} AS hora, COUNT(*) AS acidentes, "
            f"{metrics['mortes']} AS mortes, {fatal_sql} AS fatais "
            f"FROM {quote_identifier(table)} WHERE {' AND '.join(where + valid)} GROUP BY 1, 2"
        )
        grouped = rows_as_dicts(conn.execute(sql, params))

        def band(hour: int | None) -> str | None:
            if hour is None:
                return None
            if faixa == "hora":
                return f"{hour:02d}h"
            return next(name for name, start, end in SHIFTS if start <= hour <= end)

        bands = (
            [f"{h:02d}h" for h in range(24)] if faixa == "hora" else [name for name, _, _ in SHIFTS]
        ) if hour_sql else [None]
        band_order = {b: i for i, b in enumerate(bands)}

        sums: dict[tuple[int, str | None], list] = {}
        for r in grouped:
            cell = sums.setdefault((r["dia"], band(r["hora"])), [0, 0, 0])
            cell[0] += r["acidentes"]
            cell[1] += r["mortes"] or 0
            cell[2] += r["fatais"] or 0
        total_acidentes = sum(c[0] for c in sums.values())
        total_mortes = sum(c[1] for c in sums.values()) if metrics["mortes"] != "NULL" else None

        def item(dia: int, name: str | None, n: int, mortes: int, fatais: int) -> dict:
            result = {"dia_semana": DAYS_OF_WEEK[dia - 1], "dia_semana_num": dia}
            if name is not None:
                result["faixa"] = name
            result.update(
                {
                    "acidentes": n,
                    "mortes": mortes if total_mortes is not None else None,
                    "acidentes_fatais": fatais if fatal else None,
                    "taxa_fatal_pct": round(100 * fatais / n, 2) if fatal and n else None,
                    "pct_do_total": round(100 * n / total_acidentes, 2) if total_acidentes else None,
                }
            )
            return result

        cells = [
            item(dia, name, *sums.get((dia, name), [0, 0, 0]))
            for dia in range(1, 8)
            for name in bands
        ]
        por_dia = [
            item(dia, None, *(sum(c[i] for (d, _), c in sums.items() if d == dia) for i in range(3)))
            for dia in range(1, 8)
        ]
        por_faixa = (
            [
                {k: v for k, v in item(1, name, *(sum(c[i] for (_, b), c in sums.items() if b == name)
                                                  for i in range(3))).items()
                 if k not in ("dia_semana", "dia_semana_num")}
                for name in bands
            ]
            if hour_sql
            else []
        )
        pool = cells if hour_sql else por_dia
        top = sorted(
            (c for c in pool if c["acidentes"] >= min_acidentes),
            key=lambda c: (-(c["mortes"] or 0), -c["acidentes"], c["dia_semana_num"], band_order.get(c.get("faixa"), 0)),
        )[:5]

        return {
            "count": len(cells) if hour_sql else 0,
            "filters": {
                "ano": ano,
                "municipio": municipio,
                "rodovia": rodovia,
                "faixa": faixa,
                "min_acidentes": min_acidentes,
            },
            "total_acidentes": total_acidentes,
            "total_mortes": total_mortes,
            "sem_horario": total_scope - total_acidentes,
            "dimensoes_indisponiveis": [] if hour_sql else ["faixa"],
            "aviso": (
                "Frequência de acidentes registrados pela PRF em rodovias federais, por dia da semana e "
                "horário da ocorrência; não é risco por viagem (não há dados de tráfego) nem causalidade. "
                "Células com poucos acidentes têm taxas instáveis. Turnos: madrugada 0h-5h59, manhã "
                "6h-11h59, tarde 12h-17h59, noite 18h-23h59. Ocorrências sem data ou hora ficam em "
                "sem_horario e fora das células."
            ),
            "data": cells if hour_sql else [],
            "por_dia_semana": por_dia,
            "por_faixa": por_faixa,
            "mais_criticos": top,
        }
    finally:
        conn.close()
