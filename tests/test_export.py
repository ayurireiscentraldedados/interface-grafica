from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import duckdb

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export_gold.py"
REQUIRED = [
    "mart_municipality_road_safety_yearly",
    "mart_highway_safety",
    "mart_highway_segment_safety",
    "mart_accident_map",
]
OPTIONAL = ["dim_municipality", "mart_weather_road_safety_pt", "mart_vehicle_road_safety"]


def make_source(path: Path, tables: list[str]) -> None:
    conn = duckdb.connect(str(path))
    conn.execute("CREATE SCHEMA gold")
    for index, name in enumerate(tables, start=1):
        conn.execute(f'CREATE TABLE gold."{name}" AS SELECT {index} AS id, \'x\' AS texto')
    conn.close()


def export(source: Path, output: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(SCRIPT), "--source", str(source), "--output", str(output)],
        capture_output=True, text=True, encoding="utf-8",
    )


def table_names(path: Path) -> set[str]:
    conn = duckdb.connect(str(path), read_only=True)
    try:
        return {r[0] for r in conn.execute("SELECT table_name FROM information_schema.tables").fetchall()}
    finally:
        conn.close()


def test_exporta_todas_as_tabelas_e_nao_grava_o_caminho_do_computador(tmp_path: Path):
    source = tmp_path / "pasta-pessoal" / "plataforma.duckdb"
    source.parent.mkdir()
    make_source(source, REQUIRED + OPTIONAL)
    output = tmp_path / "saida.duckdb"
    result = export(source, output)
    assert result.returncode == 0, result.stdout + result.stderr
    assert table_names(output) == set(REQUIRED + OPTIONAL + ["api_metadata"])
    conn = duckdb.connect(str(output), read_only=True)
    metadata = dict(conn.execute("SELECT key, value FROM api_metadata").fetchall())
    conn.close()
    assert metadata["source_database"] == "plataforma.duckdb"
    assert "pasta-pessoal" not in " ".join(metadata.values())
    assert set(metadata["copied_tables"].split(",")) == set(REQUIRED + OPTIONAL)


def test_tabelas_opcionais_ausentes_sao_puladas(tmp_path: Path):
    source = tmp_path / "origem.duckdb"
    make_source(source, REQUIRED)
    output = tmp_path / "saida.duckdb"
    result = export(source, output)
    assert result.returncode == 0
    assert "[skip] mart_weather_road_safety_pt" in result.stdout
    assert table_names(output) == set(REQUIRED + ["api_metadata"])


def test_tabela_obrigatoria_ausente_falha_e_nao_deixa_arquivo(tmp_path: Path):
    source = tmp_path / "origem.duckdb"
    make_source(source, [t for t in REQUIRED if t != "mart_highway_safety"] + OPTIONAL)
    output = tmp_path / "saida.duckdb"
    result = export(source, output)
    assert result.returncode != 0
    assert "mart_highway_safety" in (result.stdout + result.stderr)
    assert not output.exists()


def test_origem_inexistente_falha(tmp_path: Path):
    result = export(tmp_path / "nao-existe.duckdb", tmp_path / "saida.duckdb")
    assert result.returncode != 0
    assert "Fonte não encontrada" in (result.stdout + result.stderr)


def test_saida_existente_e_substituida(tmp_path: Path):
    source = tmp_path / "origem.duckdb"
    make_source(source, REQUIRED)
    output = tmp_path / "saida.duckdb"
    antigo = duckdb.connect(str(output))
    antigo.execute("CREATE TABLE lixo AS SELECT 1 AS a")
    antigo.close()
    assert export(source, output).returncode == 0
    assert "lixo" not in table_names(output)
