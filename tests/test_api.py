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


def _client_for(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, municipal_sql: str) -> TestClient:
    db = tmp_path / "custom.duckdb"
    conn = duckdb.connect(str(db))
    conn.execute(f"CREATE TABLE mart_municipality_road_safety_yearly AS {municipal_sql}")
    conn.close()
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(db))
    monkeypatch.setenv("ACCESS_LOG_PATH", str(tmp_path / "access.csv"))
    from app.main import app
    return TestClient(app)


@pytest.fixture()
def client_sem_populacao(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    return _client_for(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES (2025, '2304400', 'Fortaleza', 100, 10, 25))
        t(year, ibge_code, municipality, accidents, deaths, serious_injuries)
    """)


@pytest.fixture()
def client_populacao_invalida(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    return _client_for(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES
            (2025, '2304400', 'Fortaleza', 100, 10, 25, 2500000),
            (2025, '9999999', 'SemDados', 5, 1, 1, 0),
            (2025, '8888888', 'PopNula', 3, 0, 0, NULL)
        ) t(year, ibge_code, municipality, accidents, deaths, serious_injuries, population)
    """)


def _client_accidents(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, accidents_sql: str) -> TestClient:
    db = tmp_path / "accidents.duckdb"
    conn = duckdb.connect(str(db))
    conn.execute(f"CREATE TABLE mart_accident_map AS {accidents_sql}")
    conn.close()
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(db))
    monkeypatch.setenv("ACCESS_LOG_PATH", str(tmp_path / "access.csv"))
    from app.main import app
    return TestClient(app)


@pytest.fixture()
def client_circunstancias(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    return _client_accidents(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES
            (1, 2025, 'Fortaleza', 'Colisão traseira', 'Velocidade incompatível', 'Seca', 'Plena noite', 1),
            (2, 2025, 'Fortaleza', 'Colisão frontal', 'Velocidade incompatível', 'Molhada', 'Plena noite', 1),
            (3, 2025, 'Fortaleza', 'Saída de leito', 'Velocidade incompatível', 'Molhada', 'Pleno dia', 1),
            (4, 2025, 'Sobral', 'Colisão traseira', 'Velocidade incompatível', 'Seca', 'Pleno dia', 0),
            (5, 2025, 'Fortaleza', 'Colisão traseira', 'Falta de atenção', 'Seca', 'Pleno dia', 0),
            (6, 2025, 'Fortaleza', 'Colisão traseira', 'Falta de atenção', 'Seca', 'Pleno dia', 0),
            (7, 2025, 'Sobral', 'Colisão traseira', 'Falta de atenção', 'Seca', 'Pleno dia', 0),
            (8, 2026, 'Sobral', 'Colisão traseira', 'Falta de atenção', 'Seca', 'Pleno dia', 0),
            (9, 2026, 'Sobral', 'Atropelamento', 'Falta de atenção', 'Seca', 'Plena noite', 1),
            (10, 2025, 'Fortaleza', 'Colisão frontal', 'Ingestão de álcool', 'Seca', 'Plena noite', 1),
            (11, 2025, 'Fortaleza', 'Capotamento', NULL, 'Seca', 'Pleno dia', 0),
            (12, 2025, 'Fortaleza', 'Capotamento', NULL, 'Seca', 'Pleno dia', 0)
        ) t(accident_key, year, municipality, accident_type, accident_cause, road_condition, lighting, deaths)
    """)


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


def test_risco_per_capita_ranking_ano(client: TestClient):
    response = client.get("/api/v1/municipios/risco-per-capita?ano=2025")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["municipality"] == "Sobral"
    assert data[0]["accidents_per_100k"] == 18.18
    assert data[1]["municipality"] == "Fortaleza"
    assert data[1]["accidents_per_100k"] == 4.0


def test_risco_per_capita_mortes_feridos(client: TestClient):
    data = client.get("/api/v1/municipios/risco-per-capita?ano=2025").json()["data"]
    fortaleza = next(r for r in data if r["municipality"] == "Fortaleza")
    assert fortaleza["deaths_per_100k"] == 0.4
    assert fortaleza["serious_injuries_per_100k"] == 1.0


def test_risco_per_capita_sem_ano(client: TestClient):
    body = client.get("/api/v1/municipios/risco-per-capita").json()
    assert body["count"] == 3
    assert body["data"][0]["municipality"] == "Sobral"


def test_risco_per_capita_ordenar_por_mortes(client: TestClient):
    data = client.get("/api/v1/municipios/risco-per-capita?ano=2025&ordenar_por=mortes").json()["data"]
    assert data[0]["municipality"] == "Sobral"
    assert data[0]["deaths_per_100k"] == 1.82


def test_risco_per_capita_ordenar_por_invalido(client: TestClient):
    response = client.get("/api/v1/municipios/risco-per-capita?ordenar_por=invalido")
    assert response.status_code == 422


def test_risco_per_capita_limit(client: TestClient):
    body = client.get("/api/v1/municipios/risco-per-capita?ano=2025&limit=1").json()
    assert body["count"] == 1
    assert body["data"][0]["municipality"] == "Sobral"


def test_risco_per_capita_sem_coluna_populacao(client_sem_populacao: TestClient):
    response = client_sem_populacao.get("/api/v1/municipios/risco-per-capita")
    assert response.status_code == 503


def test_risco_per_capita_populacao_zero_ou_nula(client_populacao_invalida: TestClient):
    data = client_populacao_invalida.get("/api/v1/municipios/risco-per-capita?ano=2025").json()["data"]
    assert data[0]["municipality"] == "Fortaleza"
    sem_dados = next(r for r in data if r["municipality"] == "SemDados")
    pop_nula = next(r for r in data if r["municipality"] == "PopNula")
    assert sem_dados["accidents_per_100k"] is None
    assert pop_nula["accidents_per_100k"] is None
    assert sem_dados["accidents"] == 5


def test_circunstancias_causa_ranking_por_fatais(client_circunstancias: TestClient):
    body = client_circunstancias.get("/api/v1/analises/circunstancias").json()
    assert body["total_acidentes"] == 12
    assert body["total_acidentes_fatais"] == 5
    top = body["data"][0]
    assert top == {
        "categoria": "Velocidade incompatível",
        "acidentes": 4,
        "acidentes_fatais": 3,
        "taxa_fatal_pct": 75.0,
        "pct_dos_acidentes_fatais": 60.0,
    }
    assert [r["categoria"] for r in body["data"]][-1] == "Não informado"


def test_circunstancias_ordenar_por_taxa_fatal(client_circunstancias: TestClient):
    data = client_circunstancias.get("/api/v1/analises/circunstancias?ordenar_por=taxa_fatal").json()["data"]
    assert data[0]["categoria"] == "Ingestão de álcool"
    assert data[0]["taxa_fatal_pct"] == 100.0


def test_circunstancias_min_acidentes(client_circunstancias: TestClient):
    url = "/api/v1/analises/circunstancias?ordenar_por=taxa_fatal&min_acidentes=2"
    data = client_circunstancias.get(url).json()["data"]
    assert data[0]["categoria"] == "Velocidade incompatível"
    assert all(r["acidentes"] >= 2 for r in data)


def test_circunstancias_filtro_ano_e_municipio(client_circunstancias: TestClient):
    body = client_circunstancias.get("/api/v1/analises/circunstancias?ano=2026").json()
    assert body["total_acidentes"] == 2
    assert body["data"][0]["pct_dos_acidentes_fatais"] == 100.0
    body = client_circunstancias.get("/api/v1/analises/circunstancias?municipio=sobral").json()
    assert body["total_acidentes"] == 4


def test_circunstancias_iluminacao(client_circunstancias: TestClient):
    body = client_circunstancias.get("/api/v1/analises/circunstancias?dimensao=iluminacao").json()
    assert body["data"][0]["categoria"] == "Plena noite"
    assert body["data"][0]["pct_dos_acidentes_fatais"] == 80.0


def test_circunstancias_dimensao_invalida(client_circunstancias: TestClient):
    response = client_circunstancias.get("/api/v1/analises/circunstancias?dimensao=clima")
    assert response.status_code == 422


def test_circunstancias_coluna_ausente(client: TestClient):
    response = client.get("/api/v1/analises/circunstancias?dimensao=causa")
    assert response.status_code == 503


def test_circunstancias_sem_gravidade(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_accidents(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES (1, 2025, 'Fortaleza', 'Seca'))
        t(accident_key, year, municipality, road_condition)
    """)
    assert c.get("/api/v1/analises/circunstancias?dimensao=condicao_pista").status_code == 503


def test_circunstancias_gravidade_por_classificacao(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_accidents(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES
            (1, 2025, 'Fortaleza', 'Chuva', 'Com Vítimas Fatais'),
            (2, 2025, 'Fortaleza', 'Chuva', 'Sem Vítimas')
        ) t(accident_key, year, municipality, road_condition, accident_classification)
    """)
    data = c.get("/api/v1/analises/circunstancias?dimensao=condicao_pista").json()["data"]
    assert data[0]["acidentes_fatais"] == 1 and data[0]["taxa_fatal_pct"] == 50.0


def _client_tables(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tables: dict[str, str]) -> TestClient:
    db = tmp_path / "tables.duckdb"
    conn = duckdb.connect(str(db))
    for name, sql in tables.items():
        conn.execute(f"CREATE TABLE {name} AS {sql}")
    conn.close()
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(db))
    monkeypatch.setenv("ACCESS_LOG_PATH", str(tmp_path / "access.csv"))
    from app.main import app
    return TestClient(app)


@pytest.fixture()
def client_perfil(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    return _client_tables(tmp_path, monkeypatch, {
        "mart_highway_safety": """
            SELECT * FROM (VALUES
                (2025, 'BR-116', 80, 8, 17),
                (2026, 'BR-116', 20, 4, 3),
                (2025, 'BR-222', 50, 5, 11),
                (2025, 'BR-020', 10, 3, 1)
            ) t(year, highway, accidents, deaths, serious_injuries)
        """,
        "mart_highway_segment_safety": """
            SELECT * FROM (VALUES
                (2025, 'BR-116', 0, 10, 20, 3),
                (2025, 'BR-116', 10, 20, 35, 5),
                (2026, 'BR-116', 0, 10, 10, 2),
                (2025, 'BR-116', 20, 30, 5, 0),
                (2025, 'BR-222', 20, 30, 12, 1)
            ) t(year, highway, segment_start_km, segment_end_km, accidents, deaths)
        """,
        "mart_accident_map": """
            SELECT * FROM (VALUES
                (1, 2025, 'BR-116', 1, 'Plena noite', 'Chuva', 'Motocicleta'),
                (2, 2025, 'BR-116', 1, 'Plena noite', 'Céu Claro', 'Motocicleta'),
                (3, 2025, 'BR-116', 0, 'Pleno dia', 'Céu Claro', 'Automóvel'),
                (4, 2026, 'BR-116', 0, 'Pleno dia', 'Céu Claro', 'Automóvel'),
                (5, 2025, 'BR-222', 0, 'Pleno dia', 'Céu Claro', 'Caminhão')
            ) t(accident_key, year, highway, deaths, lighting, weather_condition, vehicle_type)
        """,
    })


def _perfil(body: dict, rodovia: str) -> dict:
    return next(p for p in body["data"] if p["rodovia"] == rodovia)


def test_perfil_rodovia_ranking_por_mortes(client_perfil: TestClient):
    body = client_perfil.get("/api/v1/analises/perfil-rodovia").json()
    assert [p["rodovia"] for p in body["data"]] == ["BR-116", "BR-222", "BR-020"]
    br116 = body["data"][0]
    assert br116["posicao"] == 1
    assert (br116["acidentes"], br116["mortes"], br116["feridos_graves"]) == (100, 12, 20)
    assert br116["mortes_por_100_acidentes"] == 12.0


def test_perfil_rodovia_ordenar_por_taxa(client_perfil: TestClient):
    url = "/api/v1/analises/perfil-rodovia?ordenar_por=mortes_por_100_acidentes"
    body = client_perfil.get(url).json()
    assert body["data"][0]["rodovia"] == "BR-020"
    assert body["data"][0]["mortes_por_100_acidentes"] == 30.0


def test_perfil_rodovia_min_acidentes_e_limit(client_perfil: TestClient):
    body = client_perfil.get("/api/v1/analises/perfil-rodovia?min_acidentes=20").json()
    assert [p["rodovia"] for p in body["data"]] == ["BR-116", "BR-222"]
    assert client_perfil.get("/api/v1/analises/perfil-rodovia?limit=1").json()["count"] == 1


def test_perfil_rodovia_filtro_ano(client_perfil: TestClient):
    body = client_perfil.get("/api/v1/analises/perfil-rodovia?ano=2025").json()
    br116 = _perfil(body, "BR-116")
    assert (br116["acidentes"], br116["mortes"]) == (80, 8)
    assert br116["ocorrencias_mapeadas"] == 3
    assert br116["pct_acidentes_fatais"] == 66.67


def test_perfil_rodovia_uma_rodovia_e_404(client_perfil: TestClient):
    body = client_perfil.get("/api/v1/analises/perfil-rodovia?rodovia=br-222").json()
    assert body["count"] == 1 and body["data"][0]["rodovia"] == "BR-222"
    assert client_perfil.get("/api/v1/analises/perfil-rodovia?rodovia=BR-999").status_code == 404


def test_perfil_rodovia_trechos_criticos(client_perfil: TestClient):
    br116 = _perfil(client_perfil.get("/api/v1/analises/perfil-rodovia").json(), "BR-116")
    assert br116["trechos_criticos"] == [
        {"km_inicial": 10, "km_final": 20, "acidentes": 35, "mortes": 5},
        {"km_inicial": 0, "km_final": 10, "acidentes": 30, "mortes": 5},
        {"km_inicial": 20, "km_final": 30, "acidentes": 5, "mortes": 0},
    ]
    two = _perfil(client_perfil.get("/api/v1/analises/perfil-rodovia?trechos=2").json(), "BR-116")
    assert len(two["trechos_criticos"]) == 2
    none = _perfil(client_perfil.get("/api/v1/analises/perfil-rodovia?trechos=0").json(), "BR-116")
    assert none["trechos_criticos"] == []


def test_perfil_rodovia_distribuicoes(client_perfil: TestClient):
    body = client_perfil.get("/api/v1/analises/perfil-rodovia").json()
    br116 = _perfil(body, "BR-116")
    assert body["dimensoes_indisponiveis"] == []
    assert br116["pct_acidentes_fatais"] == 50.0
    assert br116["predominantes"]["clima"] == "Céu Claro"
    assert br116["distribuicoes"]["clima"][0] == {"categoria": "Céu Claro", "acidentes": 3, "pct": 75.0}
    assert br116["predominantes"]["horario"] == "Plena noite"
    assert set(br116["predominantes"]) == {"horario", "clima", "tipo_veiculo"}


def test_perfil_rodovia_sem_colunas_do_mapa(client: TestClient):
    body = client.get("/api/v1/analises/perfil-rodovia").json()
    assert body["dimensoes_indisponiveis"] == ["horario", "clima", "tipo_veiculo"]
    assert body["data"][0]["distribuicoes"] == {}
    assert body["data"][0]["pct_acidentes_fatais"] is None
    assert body["data"][0]["trechos_criticos"]


def test_perfil_rodovia_ordenar_por_invalido(client_perfil: TestClient):
    assert client_perfil.get("/api/v1/analises/perfil-rodovia?ordenar_por=x").status_code == 422


def test_perfil_rodovia_sem_coluna_de_mortes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_highway_safety": """
            SELECT * FROM (VALUES (2025, 'BR-116', 80), (2025, 'BR-222', 50)) t(year, highway, accidents)
        """,
    })
    assert c.get("/api/v1/analises/perfil-rodovia").status_code == 503
    body = c.get("/api/v1/analises/perfil-rodovia?ordenar_por=acidentes").json()
    assert body["data"][0]["rodovia"] == "BR-116"
    assert body["data"][0]["mortes"] is None


# ---------- erros nas rotas já existentes ----------

@pytest.mark.parametrize("url", [
    "/api/v1/municipios?limit=0",
    "/api/v1/municipios?limit=501",
    "/api/v1/municipios?ano=1999",
    "/api/v1/municipios?ano=abc",
    "/api/v1/municipios/2304400/indicadores?ano=1999",
    "/api/v1/rodovias?limit=101",
    "/api/v1/rodovias?ano=2101",
    "/api/v1/trechos-criticos?limit=0",
    "/api/v1/acidentes?limit=501",
    "/api/v1/acidentes?offset=-1",
])
def test_parametro_invalido_retorna_422(client: TestClient, url: str):
    assert client.get(url).status_code == 422


def test_indicadores_de_municipio_inexistente_retorna_404(client: TestClient):
    response = client.get("/api/v1/municipios/0000000/indicadores")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_indicadores_de_ano_sem_dado_retorna_404(client: TestClient):
    assert client.get("/api/v1/municipios/2304400/indicadores?ano=2024").status_code == 404


def test_rota_inexistente_retorna_404(client: TestClient):
    assert client.get("/api/v1/nao-existe").status_code == 404


def test_rota_so_aceita_leitura(client: TestClient):
    assert client.post("/api/v1/municipios").status_code == 405


def test_banco_ausente_retorna_503_e_health_degradado(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(tmp_path / "nao-existe.duckdb"))
    monkeypatch.setenv("ACCESS_LOG_PATH", str(tmp_path / "access.csv"))
    from app.main import app
    c = TestClient(app)
    assert c.get("/api/v1/municipios").status_code == 503
    assert c.get("/api/v1/analises/perfil-rodovia").status_code == 503
    health = c.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "degraded"


def test_tabela_ausente_retorna_503(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_municipality_road_safety_yearly": "SELECT 2025 AS year, 'x' AS ibge_code, 'Y' AS municipality",
    })
    response = c.get("/api/v1/rodovias")
    assert response.status_code == 503
    assert "mart_highway_safety" in response.json()["detail"]


def test_esquema_incompativel_retorna_500_explicando(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_municipality_road_safety_yearly": "SELECT 2025 AS year, 10 AS accidents",
    })
    response = c.get("/api/v1/municipios")
    assert response.status_code == 500
    assert response.json()["detail"]["error"] == "schema_incompativel"


# ---------- nome da rodovia: "116" e "BR-116" valem igual ----------

@pytest.mark.parametrize("nome", ["BR-116", "br-116", "116", "BR 116"])
def test_filtro_de_rodovia_aceita_as_duas_formas_no_trechos(client: TestClient, nome: str):
    body = client.get("/api/v1/trechos-criticos", params={"rodovia": nome}).json()
    assert body["count"] == 1 and body["data"][0]["highway"] == "BR-116"


def test_filtro_de_rodovia_com_nome_numerico_no_banco(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_highway_safety": "SELECT * FROM (VALUES (2025, 116, 80, 8), (2025, 222, 50, 5)) t(year, highway, accidents, deaths)",
    })
    for nome in ("BR-116", "116"):
        body = c.get("/api/v1/analises/perfil-rodovia", params={"rodovia": nome}).json()
        assert body["count"] == 1 and body["data"][0]["rodovia"] == "116"


# ---------- registro de acessos ----------

def test_acesso_vai_para_o_csv_e_para_a_saida_do_servico(client: TestClient, capsys: pytest.CaptureFixture):
    client.get("/api/v1/municipios?ano=2025")
    saida = capsys.readouterr().out
    assert "ACESSO " in saida and " GET /api/v1/municipios 200 " in saida
    assert "ano=2025" not in saida
    linhas = Path(os.environ["ACCESS_LOG_PATH"]).read_text(encoding="utf-8").splitlines()
    assert linhas[0] == "timestamp_utc,method,path,status,duration_ms"
    assert ",GET,/api/v1/municipios,200," in linhas[1]


def test_resumo_de_acessos_junta_fontes_sem_contar_duas_vezes(tmp_path: Path):
    import subprocess, sys
    script = Path(__file__).resolve().parents[1] / "scripts" / "summarize_access.py"
    csv_log = tmp_path / "access.csv"
    csv_log.write_text(
        "timestamp_utc,method,path,status,duration_ms\n"
        "2026-11-01T10:00:00+00:00,GET,/api/v1/municipios,200,5.0\n"
        "2026-11-01T10:01:00+00:00,GET,/health,200,1.0\n",
        encoding="utf-8",
    )
    render_log = tmp_path / "render.txt"
    render_log.write_text(
        "Nov 01 07:00:00 api-1 | ACESSO 2026-11-01T10:00:00+00:00 GET /api/v1/municipios 200 5.0\n"
        "Nov 02 07:00:00 api-1 | ACESSO 2026-11-02T09:00:00+00:00 GET /api/v1/rodovias 200 7.5\n"
        "Nov 02 07:01:00 api-1 | ACESSO 2026-11-02T09:01:00+00:00 GET /api/v1/rodovias 404 2.0\n"
        "Nov 02 07:02:00 api-1 | ACESSO 2026-11-02T09:02:00+00:00 GET /docs 200 2.0\n"
        "Nov 02 07:03:00 api-1 | INFO: linha qualquer\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(script), "--log", str(csv_log), "--render-log", str(render_log)],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    assert "Consultas úteis bem-sucedidas: 2" in result.stdout
    assert "2026-11-01T10:00:00 até 2026-11-02T09:00:00" in result.stdout
    assert "/api/v1/rodovias" in result.stdout


# ---------- cache das colunas e registro de acessos do uvicorn ----------

def test_colunas_do_catalogo_sao_guardadas_em_memoria(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from app import db
    path = tmp_path / "cache.duckdb"
    c = duckdb.connect(str(path))
    c.execute("CREATE TABLE t AS SELECT 1 AS a, 2 AS b")
    c.close()
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(path))

    class Contador:
        def __init__(self, conn):
            self.conn, self.chamadas = conn, 0

        def execute(self, *args):
            self.chamadas += 1
            return self.conn.execute(*args)

    conn = duckdb.connect(str(path), read_only=True)
    contador = Contador(conn)
    colunas = db.columns(contador, "t")
    assert colunas == ["a", "b"]
    colunas.append("mexeu")
    assert db.columns(contador, "t") == ["a", "b"]
    assert db.table_exists(contador, "t") is True
    assert db.table_exists(contador, "nao_existe") is False
    assert db.table_exists(contador, "nao_existe") is False
    assert contador.chamadas == 2
    conn.close()


def test_cache_de_colunas_renova_quando_o_banco_e_trocado(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import time
    from app import db
    path = tmp_path / "troca.duckdb"
    monkeypatch.setenv("ROAD_SAFETY_DB_PATH", str(path))

    def criar(sql: str):
        if path.exists():
            path.unlink()
        c = duckdb.connect(str(path))
        c.execute(sql)
        c.close()

    def ler() -> list[str]:
        conn = duckdb.connect(str(path), read_only=True)
        try:
            return db.columns(conn, "t")
        finally:
            conn.close()

    criar("CREATE TABLE t AS SELECT 1 AS a")
    assert ler() == ["a"]
    time.sleep(0.05)
    criar("CREATE TABLE t AS SELECT 1 AS a, 2 AS novo")
    assert ler() == ["a", "novo"]


def test_registro_de_acessos_do_uvicorn_fica_desligado():
    import logging
    from app.main import app  # noqa: F401
    assert logging.getLogger("uvicorn.access").disabled is True


# ---------- empates: a mesma consulta sempre devolve a mesma ordem ----------

def test_rodovias_com_empate_desempata_por_mortes_depois_feridos(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_highway_safety": """
            SELECT * FROM (VALUES
                (2025, 'BR-B', 50, 3, 1),
                (2025, 'BR-C', 50, 3, 2),
                (2025, 'BR-A', 50, 9, 1),
                (2025, 'BR-D', 70, 1, 1)
            ) t(year, highway, accidents, deaths, serious_injuries)
        """,
    })
    ordem = [r["highway"] for r in c.get("/api/v1/rodovias").json()["data"]]
    assert ordem == ["BR-D", "BR-A", "BR-C", "BR-B"]
    assert [r["highway"] for r in c.get("/api/v1/rodovias?limit=3").json()["data"]] == ["BR-D", "BR-A", "BR-C"]


def test_trechos_com_empate_desempata_por_mortes_rodovia_e_km(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_tables(tmp_path, monkeypatch, {
        "mart_highway_segment_safety": """
            SELECT * FROM (VALUES
                (2025, 'BR-222', 20, 30, 10, 1),
                (2025, 'BR-116', 10, 20, 10, 1),
                (2025, 'BR-116', 0, 10, 10, 1),
                (2025, 'BR-020', 0, 10, 10, 4)
            ) t(year, highway, segment_start_km, segment_end_km, accidents, deaths)
        """,
    })
    dados = c.get("/api/v1/trechos-criticos").json()["data"]
    assert [(r["highway"], r["segment_start_km"]) for r in dados] == [
        ("BR-020", 0), ("BR-116", 0), ("BR-116", 10), ("BR-222", 20),
    ]


def test_acidentes_paginam_em_ordem_fixa(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_accidents(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES (3, 2025, 'X'), (1, 2025, 'X'), (2, 2025, 'X')) t(accident_key, year, municipality)
    """)
    assert [r["accident_key"] for r in c.get("/api/v1/acidentes").json()["data"]] == [1, 2, 3]
    assert [r["accident_key"] for r in c.get("/api/v1/acidentes?limit=1&offset=1").json()["data"]] == [2]
    assert [r["accident_key"] for r in c.get("/api/v1/acidentes?limit=5&offset=2").json()["data"]] == [3]


def test_risco_per_capita_com_empate_ordena_por_nome(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    c = _client_for(tmp_path, monkeypatch, """
        SELECT * FROM (VALUES
            (2025, '2', 'Zeta', 10, 0, 0, 1000),
            (2025, '1', 'Alfa', 10, 0, 0, 1000),
            (2025, '3', 'Meio', 10, 0, 0, 1000)
        ) t(year, ibge_code, municipality, accidents, deaths, serious_injuries, population)
    """)
    dados = c.get("/api/v1/municipios/risco-per-capita").json()["data"]
    assert [r["municipality"] for r in dados] == ["Alfa", "Meio", "Zeta"]
