from __future__ import annotations

import os
from pathlib import Path

import duckdb
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db = tmp_path / "fixture.duckdb"
    conn = duckdb.connect(str(db))
    conn.execute("""
        CREATE TABLE mart_municipality_road_safety_yearly AS
        SELECT * FROM (VALUES
            (2025, '2304400', 'Fortaleza', 100, 10, 25, 2500000),
            (2025, '2312908', 'Sobral', 40, 4, 9, 220000),
            (2026, '2304400', 'Fortaleza', 60, 7, 14, 2600000)
        ) t(year, ibge_code, municipality, accidents, deaths, serious_injuries, population)
    """)
    conn.execute("""
        CREATE TABLE mart_highway_safety AS
        SELECT * FROM (VALUES
            (2025, 'BR-116', 80, 8, 17),
            (2025, 'BR-222', 50, 5, 11)
        ) t(year, highway, accidents, deaths, serious_injuries)
    """)
    conn.execute("""
        CREATE TABLE mart_highway_segment_safety AS
        SELECT * FROM (VALUES
            (2025, 'BR-116', 0.0, 10.0, 20, 3),
            (2025, 'BR-222', 20.0, 30.0, 12, 1)
        ) t(year, highway, segment_start_km, segment_end_km, accidents, deaths)
    """)
    conn.execute("""
        CREATE TABLE mart_accident_map AS
        SELECT * FROM (VALUES
            ('a1', 2025, 'Fortaleza', '2304400', 'BR-116', -3.73, -38.52),
            ('a2', 2025, 'Sobral', '2312908', 'BR-222', -3.69, -40.35)
        ) t(accident_key, year, municipality, ibge_code, highway, map_latitude, map_longitude)
    """)
    conn.close()

    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(db))
    monkeypatch.setenv("ACCESS_LOG_PATH", str(tmp_path / "access.csv"))

    from app.main import app
    return TestClient(app)


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_municipalities(client: TestClient):
    response = client.get("/api/v1/municipios?ano=2025")
    assert response.status_code == 200
    assert response.json()["count"] == 2


def test_municipality_indicators(client: TestClient):
    response = client.get("/api/v1/municipios/2304400/indicadores?ano=2025")
    assert response.status_code == 200
    assert response.json()["data"][0]["municipality"] == "Fortaleza"


def test_highway_ranking(client: TestClient):
    response = client.get("/api/v1/rodovias?ano=2025&limit=1")
    assert response.status_code == 200
    assert response.json()["data"][0]["highway"] == "BR-116"


def test_accident_filter(client: TestClient):
    response = client.get("/api/v1/acidentes?ano=2025&municipio=Sobral")
    assert response.status_code == 200
    assert response.json()["count"] == 1
