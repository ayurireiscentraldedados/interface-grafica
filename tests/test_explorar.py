"""Smoke tests de integração para a consulta guiada (/explorar)."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.explorer import router


def test_pagina_pode_ser_servida_sem_banco():
    app = FastAPI()
    app.include_router(router)
    response = TestClient(app).get('/explorar')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/html')
    assert response.headers['x-content-type-options'] == 'nosniff'
    assert '<html lang="pt-BR">' in response.text


def test_conteudo_publico_e_acessivel():
    app = FastAPI()
    app.include_router(router)
    response = TestClient(app).get('/explorar')
    html = response.text
    for marker in ('href="#principal"', 'role="status"', 'aria-live="polite"',
                   'role="tablist"', 'aria-label="Tipos de consulta"',
                   'id="municipio"', 'id="ano"', 'id="consulta"',
                   'prefers-reduced-motion', '31/08/2026', 'rodovias federais'):
        assert marker in html


def test_fonte_dados_respeita_estrutura_existente():
    app = FastAPI()
    app.include_router(router)
    html = TestClient(app).get('/explorar').text
    assert '/api/v1/municipios?ano=2025&limit=500' in html
    assert '/indicadores?ano=' in html
    assert '/api/v1/rodovias?ano=' in html
    assert '/api/v1/trechos-criticos?ano=' in html
    assert 'textContent' in html
    assert 'innerHTML' not in html  # impede interpolação de dados em HTML


def test_rota_real_registrada_quando_dependencias_disponiveis():
    from app.main import app
    response = TestClient(app).get('/explorar')
    assert response.status_code == 200
    assert 'Acidentes nas rodovias do Ceará' in response.text
    assert '/explorar' not in app.openapi()['paths']  # não poluir o Swagger

def test_home_redireciona_navegadores_e_preserva_api():
    from app.main import app
    client = TestClient(app)
    browser = client.get('/', headers={'accept': 'text/html'}, follow_redirects=False)
    assert browser.status_code == 307
    assert browser.headers['location'] == '/explorar'
    assert client.get('/explorar').status_code == 200
    api = client.get('/', headers={'accept': 'application/json'})
    assert api.status_code == 200
    assert api.json()['explorar'] == '/explorar'
    assert client.get('/docs').status_code == 200

def test_municipio_nao_vem_preenchido_com_a_primeira_tarefa():
    """O exemplo Fortaleza era exatamente a primeira tarefa do estudo externo."""
    app = FastAPI()
    app.include_router(router)
    html = TestClient(app).get('/explorar').text
    assert 'id="busca-municipio"' in html
    assert 'value="Fortaleza"' not in html
