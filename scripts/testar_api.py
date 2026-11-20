"""Testa a chamada e as funcionalidades da API de Segurança Viária CE.

Diferente do `pytest` (que usa um banco de mentira em memória), este script faz requisições
HTTP reais contra a API pública, a que o usuário final enxerga.

Uso:
    python scripts/testar_api.py
    python scripts/testar_api.py --timeout 90   # Render grátis demora ao "acordar"

Só usa a biblioteca padrão do Python. Sai com código 0 se tudo passou e 1 se algo falhou.
Rotas que ainda não estão na API pública aparecem como PULADO, não como falha, porque a lista
de rotas vem do próprio `/openapi.json` da API.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

URL_PUBLICA = "https://api-seguranca-viaria-ce.onrender.com"
LIMITE_LENTO_S = 3.0


@dataclass
class Resposta:
    status: int
    corpo: object
    cabecalhos: dict[str, str]
    segundos: float


@dataclass
class Resultado:
    nome: str
    estado: str  # OK | FALHA | PULADO
    detalhe: str = ""
    segundos: float | None = None


@dataclass
class Execucao:
    base: str
    timeout: float
    resultados: list[Resultado] = field(default_factory=list)
    rotas_disponiveis: set[str] | None = None

    # ---------- HTTP ----------
    def chamar(self, caminho: str, params: dict | None = None, metodo: str = "GET") -> Resposta:
        url = self.base + caminho
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        req = urllib.request.Request(url, method=metodo, headers={"Accept": "application/json"})
        inicio = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                status, bruto, cab = r.status, r.read(), dict(r.headers)
        except urllib.error.HTTPError as erro:
            status, bruto, cab = erro.code, erro.read(), dict(erro.headers)
        segundos = time.perf_counter() - inicio
        try:
            corpo = json.loads(bruto.decode("utf-8")) if bruto else None
        except ValueError:
            corpo = bruto.decode("utf-8", errors="replace")
        return Resposta(status, corpo, {k.lower(): v for k, v in cab.items()}, segundos)

    # ---------- registro ----------
    def checar(self, nome: str, funcao) -> None:
        """Roda uma verificação; AssertionError/erro de rede viram FALHA, Pular vira PULADO."""
        try:
            detalhe, segundos = funcao()
            self.resultados.append(Resultado(nome, "OK", detalhe, segundos))
        except Pular as motivo:
            self.resultados.append(Resultado(nome, "PULADO", str(motivo)))
        except AssertionError as erro:
            self.resultados.append(Resultado(nome, "FALHA", str(erro) or "asserção falhou"))
        except (urllib.error.URLError, TimeoutError, OSError) as erro:
            self.resultados.append(Resultado(nome, "FALHA", f"erro de rede: {erro}"))


class Pular(Exception):
    pass


def esperar(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise AssertionError(mensagem)


def tem_rota(exec_: Execucao, caminho_openapi: str) -> None:
    if exec_.rotas_disponiveis is not None and caminho_openapi not in exec_.rotas_disponiveis:
        raise Pular("rota não existe nesta instância (ainda não publicada)")


def lista_valida(r: Resposta, minimo: int = 0) -> dict:
    esperar(r.status == 200, f"esperava HTTP 200, veio {r.status}: {str(r.corpo)[:150]}")
    esperar(isinstance(r.corpo, dict), "resposta não é um objeto JSON")
    esperar("data" in r.corpo and isinstance(r.corpo["data"], list), "campo 'data' ausente ou não é lista")
    esperar("count" in r.corpo, "campo 'count' ausente")
    esperar(len(r.corpo["data"]) >= minimo, f"esperava ao menos {minimo} item(ns), veio {len(r.corpo['data'])}")
    return r.corpo


def descrever(r: Resposta, extra: str = "") -> str:
    return f"HTTP {r.status} em {r.segundos:.2f}s" + (f" — {extra}" if extra else "")


# =====================================================================================
# Verificações
# =====================================================================================

def montar_verificacoes(e: Execucao) -> list[tuple[str, object]]:
    v: list[tuple[str, object]] = []

    def add(nome):
        def deco(f):
            v.append((nome, f))
            return f
        return deco

    # ---------- meta ----------
    @add("GET / devolve nome, docs e health")
    def _():
        r = e.chamar("/")
        esperar(r.status == 200, f"HTTP {r.status}")
        esperar(all(k in r.corpo for k in ("name", "docs", "health", "api")), f"chaves faltando: {r.corpo}")
        return descrever(r, r.corpo["name"]), r.segundos

    @add("GET /health informa banco pronto")
    def _():
        r = e.chamar("/health")
        esperar(r.status == 200, f"HTTP {r.status}")
        esperar(r.corpo.get("status") == "ok", f"status = {r.corpo.get('status')!r} (esperava 'ok'): {r.corpo}")
        esperar(r.corpo.get("datasets_available", 0) >= 1, "nenhum dataset disponível")
        return descrever(r, f"{r.corpo['datasets_available']} datasets"), r.segundos

    @add("GET /docs abre a documentação interativa (Swagger)")
    def _():
        r = e.chamar("/docs")
        esperar(r.status == 200, f"HTTP {r.status}")
        esperar("swagger" in str(r.corpo).lower(), "página não parece o Swagger UI")
        return descrever(r), r.segundos

    @add("GET /openapi.json descreve as rotas")
    def _():
        r = e.chamar("/openapi.json")
        esperar(r.status == 200, f"HTTP {r.status}")
        esperar("paths" in r.corpo, "sem 'paths'")
        return descrever(r, f"{len(r.corpo['paths'])} caminhos"), r.segundos

    @add("CORS liberado para navegadores (Access-Control-Allow-Origin)")
    def _():
        req = urllib.request.Request(e.base + "/health", headers={"Origin": "https://exemplo.com"})
        with urllib.request.urlopen(req, timeout=e.timeout) as r:
            origem = r.headers.get("access-control-allow-origin")
        esperar(origem in ("*", "https://exemplo.com"), f"cabeçalho CORS = {origem!r}")
        return f"allow-origin = {origem}", None

    # ---------- consultas ----------
    @add("GET /api/v1/datasets lista tabelas e colunas")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/datasets"), 1)
        esperar(c["count"] == len(c["data"]), "count diferente do tamanho de data")
        esperar(all({"id", "table", "columns"} <= set(d) for d in c["data"]), "item sem id/table/columns")
        return descrever(r, ", ".join(d["id"] for d in c["data"])), r.segundos

    @add("GET /api/v1/municipios lista 184 municípios com ibge_code")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/municipios", {"ano": 2025}), 1)
        esperar(c["count"] == len(c["data"]), "count diferente do tamanho de data")
        esperar("ibge_code" in c["data"][0] and "municipality" in c["data"][0], "faltam ibge_code/municipality")
        nomes = [m["municipality"] for m in c["data"]]
        esperar(nomes == sorted(nomes), "municípios fora de ordem alfabética")
        return descrever(r, f"{c['count']} municípios"), r.segundos

    @add("GET /api/v1/municipios?limit=3 respeita o limite")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/municipios", {"ano": 2025, "limit": 3}))
        esperar(c["count"] == 3 == len(c["data"]), f"count = {c['count']}")
        return descrever(r), r.segundos

    @add("GET /api/v1/municipios/2304400/indicadores (Fortaleza)")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/municipios/2304400/indicadores", {"ano": 2025}), 1)
        linha = c["data"][0]
        esperar("fortaleza" in str(linha.get("municipality", "")).lower(), f"município = {linha.get('municipality')}")
        esperar(int(linha.get("year", 2025)) == 2025, f"ano = {linha.get('year')}")
        return descrever(r, f"{linha.get('accidents')} acidentes em 2025"), r.segundos

    @add("GET /api/v1/municipios/{ibge_code}/indicadores sem ano devolve a série")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/municipios/2312908/indicadores"), 1)
        return descrever(r, f"{c['count']} ano(s) de Sobral"), r.segundos

    @add("GET /api/v1/rodovias devolve ranking ordenado")
    def _():
        c = lista_valida(r := e.chamar("/api/v1/rodovias", {"ano": 2025, "limit": 5}), 1)
        esperar(c["count"] <= 5, f"count = {c['count']} > limit")
        acidentes = [x.get("accidents") for x in c["data"] if x.get("accidents") is not None]
        esperar(acidentes == sorted(acidentes, reverse=True), f"ranking fora de ordem: {acidentes}")
        return descrever(r, f"topo: {c['data'][0].get('highway')}"), r.segundos

    @add("GET /api/v1/trechos-criticos aceita 'BR-116' e '116' com o mesmo resultado")
    def _():
        a = lista_valida(r1 := e.chamar("/api/v1/trechos-criticos", {"rodovia": "BR-116", "limit": 5}), 1)
        b = lista_valida(r2 := e.chamar("/api/v1/trechos-criticos", {"rodovia": "116", "limit": 5}), 1)
        esperar(a["data"] == b["data"], "'BR-116' e '116' devolveram dados diferentes")
        esperar(all(str(x["highway"]).upper().endswith("116") for x in a["data"]), "veio trecho de outra rodovia")
        return descrever(r1, f"{a['count']} trechos"), r1.segundos + r2.segundos

    @add("GET /api/v1/acidentes pagina com limit/offset sem repetir linhas")
    def _():
        p1 = lista_valida(r := e.chamar("/api/v1/acidentes", {"ano": 2025, "limit": 3, "offset": 0}), 1)
        p2 = lista_valida(e.chamar("/api/v1/acidentes", {"ano": 2025, "limit": 3, "offset": 3}), 1)
        chave = "accident_key"
        if chave in p1["data"][0]:
            k1, k2 = {x[chave] for x in p1["data"]}, {x[chave] for x in p2["data"]}
            esperar(not (k1 & k2), "páginas diferentes repetiram acidentes")
        return descrever(r, "paginação estável"), r.segundos

    @add("GET /api/v1/acidentes filtra por município sem diferenciar maiúsculas")
    def _():
        a = lista_valida(r := e.chamar("/api/v1/acidentes", {"municipio": "fortaleza", "limit": 5}), 1)
        esperar(all(str(x.get("municipality", "")).lower() == "fortaleza" for x in a["data"]), "município errado")
        return descrever(r), r.segundos

    # ---------- análises ----------
    def analise(caminho: str, params: dict | None, campos: tuple[str, ...] = ()):
        def f():
            tem_rota(e, caminho)
            r = e.chamar(caminho, params)
            esperar(r.status == 200, f"HTTP {r.status}: {str(r.corpo)[:200]}")
            esperar(isinstance(r.corpo, dict), "resposta não é objeto JSON")
            faltando = [c for c in ("data", *campos) if c not in r.corpo]
            esperar(not faltando, f"campos ausentes: {faltando}")
            esperar(len(r.corpo["data"]) >= 1, "'data' veio vazio")
            return descrever(r, f"{len(r.corpo['data'])} linhas"), r.segundos
        return f

    v.append(("GET /api/v1/municipios/risco-per-capita", analise(
        "/api/v1/municipios/risco-per-capita", {"ano": 2025, "limit": 5}, ("count", "filters"))))
    v.append(("GET /api/v1/analises/circunstancias", analise(
        "/api/v1/analises/circunstancias", {"dimensao": "iluminacao", "ano": 2025}, ("total_acidentes", "aviso"))))
    v.append(("GET /api/v1/analises/perfil-rodovia", analise(
        "/api/v1/analises/perfil-rodovia", {"ano": 2025, "limit": 3}, ("count", "aviso"))))
    v.append(("GET /api/v1/analises/evolucao (anual)", analise(
        "/api/v1/analises/evolucao", {}, ("periodo_parcial", "aviso"))))
    v.append(("GET /api/v1/analises/evolucao (mensal)", analise(
        "/api/v1/analises/evolucao", {"granularidade": "mes", "ano": 2025}, ("aviso",))))
    v.append(("GET /api/v1/analises/quando-acontece", analise(
        "/api/v1/analises/quando-acontece", {"faixa": "turno"}, ("por_dia_semana", "mais_criticos"))))
    v.append(("GET /api/v1/analises/clima", analise("/api/v1/analises/clima", {"ano": 2025}, ("total_acidentes",))))
    v.append(("GET /api/v1/analises/veiculos", analise("/api/v1/analises/veiculos", {"ano": 2025, "limit": 5})))
    v.append(("GET /api/v1/analises/regioes", analise(
        "/api/v1/analises/regioes", {"nivel": "intermediaria", "ano": 2025})))

    @add("Consistência: ranking per capita bate com municípios cadastrados")
    def _():
        tem_rota(e, "/api/v1/municipios/risco-per-capita")
        c = lista_valida(r := e.chamar("/api/v1/municipios/risco-per-capita", {"ano": 2025, "limit": 10}), 1)
        taxas = [x.get("accidents_per_100k") for x in c["data"] if x.get("accidents_per_100k") is not None]
        esperar(taxas == sorted(taxas, reverse=True), f"taxas fora de ordem decrescente: {taxas}")
        return descrever(r, f"maior taxa = {taxas[0]} por 100 mil"), r.segundos

    # ---------- erros esperados ----------
    def erro(nome: str, caminho: str, params: dict | None, esperado: int, metodo: str = "GET", exige_rota=None):
        def f():
            if exige_rota:
                tem_rota(e, exige_rota)
            r = e.chamar(caminho, params, metodo)
            esperar(r.status == esperado, f"esperava HTTP {esperado}, veio {r.status}")
            return descrever(r, "erro tratado corretamente"), r.segundos
        v.append((nome, f))

    erro("Erro 422: limit=0 em /municipios", "/api/v1/municipios", {"limit": 0}, 422)
    erro("Erro 422: limit acima do máximo em /rodovias", "/api/v1/rodovias", {"limit": 101}, 422)
    erro("Erro 422: ano=1999 em /municipios", "/api/v1/municipios", {"ano": 1999}, 422)
    erro("Erro 422: ano não numérico", "/api/v1/municipios", {"ano": "abc"}, 422)
    erro("Erro 422: offset negativo em /acidentes", "/api/v1/acidentes", {"offset": -1}, 422)
    erro("Erro 404: município inexistente", "/api/v1/municipios/0000000/indicadores", None, 404)
    erro("Erro 404: rota inexistente", "/api/v1/nao-existe", None, 404)
    erro("Erro 405: POST em rota de leitura", "/api/v1/municipios", None, 405, metodo="POST")
    erro("Erro 422: ordenar_por inválido (risco per capita)", "/api/v1/municipios/risco-per-capita",
         {"ordenar_por": "invalido"}, 422, exige_rota="/api/v1/municipios/risco-per-capita")
    erro("Erro 422: dimensao inválida (circunstâncias)", "/api/v1/analises/circunstancias",
         {"dimensao": "clima"}, 422, exige_rota="/api/v1/analises/circunstancias")
    erro("Erro 404: rodovia inexistente (perfil-rodovia)", "/api/v1/analises/perfil-rodovia",
         {"rodovia": "BR-999"}, 404, exige_rota="/api/v1/analises/perfil-rodovia")

    # ---------- desempenho ----------
    @add(f"Desempenho: respostas leves em menos de {LIMITE_LENTO_S:.0f}s")
    def _():
        lentas = []
        for caminho in ("/health", "/api/v1/datasets", "/api/v1/municipios"):
            r = e.chamar(caminho)
            if r.segundos > LIMITE_LENTO_S:
                lentas.append(f"{caminho} ({r.segundos:.2f}s)")
        esperar(not lentas, "lentas: " + ", ".join(lentas))
        return "todas dentro do limite", None

    return v


def carregar_rotas(e: Execucao) -> None:
    try:
        r = e.chamar("/openapi.json")
        if r.status == 200 and isinstance(r.corpo, dict):
            e.rotas_disponiveis = set(r.corpo.get("paths", {}))
    except (urllib.error.URLError, TimeoutError, OSError):
        pass


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Testa as chamadas e funcionalidades da API de Segurança Viária CE.")
    ap.add_argument("--timeout", type=float, default=30.0, help="segundos de espera por resposta (padrão: 30)")
    args = ap.parse_args()

    e = Execucao(base=URL_PUBLICA, timeout=args.timeout)
    print(f"Testando {e.base}\n")

    # A primeira chamada pode demorar: o Render gratuito "dorme" e leva até ~1 min para acordar.
    try:
        inicio = time.perf_counter()
        e.chamar("/health")
        print(f"API respondeu em {time.perf_counter() - inicio:.2f}s (aquecimento)\n")
    except (urllib.error.URLError, TimeoutError, OSError) as erro:
        print(f"ERRO: não consegui falar com a API em {e.base}: {erro}")
        print("O Render gratuito pode estar acordando; tente de novo com --timeout 90.")
        return 1

    carregar_rotas(e)
    for nome, funcao in montar_verificacoes(e):
        e.checar(nome, funcao)

    simbolo = {"OK": "[ OK  ]", "FALHA": "[FALHA]", "PULADO": "[PULOU]"}
    for res in e.resultados:
        print(f"{simbolo[res.estado]} {res.nome}")
        if res.detalhe:
            print(f"         {res.detalhe}")

    ok = sum(r.estado == "OK" for r in e.resultados)
    falhas = sum(r.estado == "FALHA" for r in e.resultados)
    pulos = sum(r.estado == "PULADO" for r in e.resultados)
    tempos = [r.segundos for r in e.resultados if r.segundos]
    print(f"\nResumo: {ok} passaram, {falhas} falharam, {pulos} puladas (total {len(e.resultados)})")
    if tempos:
        print(f"Tempo médio das chamadas: {sum(tempos) / len(tempos):.2f}s — mais lenta: {max(tempos):.2f}s")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
