"""Testes da auditoria; sem inferir participação humana a partir de arquivos."""
import csv
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "auditar_evidencias.py"
spec = importlib.util.spec_from_file_location("auditar_evidencias", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def preparar(tmp_path, **campos):
    base = {
        "data": "2026-11-23", "tipo": "qualitativa", "indicador": "teste externo",
        "canal": "formulario", "quem_de_fora": "estudante externo",
        "valor": "", "descricao": "relato autorizado", "arquivo": "evidencias/prova.txt",
    }
    base.update(campos)
    (tmp_path / "evidencias").mkdir()
    with (tmp_path / "evidencias.csv").open("w", encoding="utf-8", newline="") as arq:
        escritor = csv.DictWriter(arq, fieldnames=list(base))
        escritor.writeheader()
        escritor.writerow(base)
    (tmp_path / "evidencias" / "prova.txt").write_text("Relato", encoding="utf-8")


def test_arquivo_referenciado_e_alerta_textual(tmp_path):
    preparar(tmp_path)
    r = mod.auditar(tmp_path)
    assert r["erros"] == 0
    assert any(a["codigo"] == "registro_textual" for a in r["achados"])


def test_arquivo_ausente(tmp_path):
    preparar(tmp_path, arquivo="evidencias/inexistente.pdf")
    assert any(a["codigo"] == "arquivo_ausente" for a in mod.auditar(tmp_path)["achados"])


def test_impede_path_traversal(tmp_path):
    preparar(tmp_path, arquivo="../../segredo.txt")
    assert any(a["codigo"] == "caminho_inseguro" for a in mod.auditar(tmp_path)["achados"])


def test_data_invalida(tmp_path):
    preparar(tmp_path, data="2026-13-55")
    assert any(a["codigo"] == "data_invalida" for a in mod.auditar(tmp_path)["achados"])


def test_contagem_exige_valor(tmp_path):
    preparar(tmp_path, tipo="contagem", valor="")
    assert any(a["codigo"] == "valor_ausente" for a in mod.auditar(tmp_path)["achados"])


def test_csv_ausente(tmp_path):
    assert mod.auditar(tmp_path)["erros"] == 1


def test_registro_completo_em_pdf(tmp_path):
    preparar(tmp_path, arquivo="evidencias/prova.pdf")
    (tmp_path / "evidencias" / "prova.pdf").write_bytes(b"%PDF-1.4\nexemplo")
    assert mod.auditar(tmp_path)["erros"] == 0
    assert mod.auditar(tmp_path)["alertas"] == 0
