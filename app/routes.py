from __future__ import annotations

import re
from typing import Annotated, Literal

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
