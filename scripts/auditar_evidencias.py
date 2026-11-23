"""Auditoria estrutural das evidências do Marco 3.

Verifica integridade de registros e arquivos referenciados. Não atesta
participação humana, autenticidade de depoimentos ou consultas externas.

Uso: python scripts/auditar_evidencias.py --root . --json saida.json
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

CAMPOS = ("data", "tipo", "indicador", "canal", "quem_de_fora", "valor", "descricao", "arquivo")
TIPOS = {"qualitativa", "quantitativa", "contagem"}


def auditar(root: Path) -> dict:
    root = root.resolve()
    entrada = root / "evidencias.csv"
    achados: list[dict[str, object]] = []

    def anotar(nivel: str, codigo: str, detalhe: str, linha: int | None = None) -> None:
        item: dict[str, object] = {"nivel": nivel, "codigo": codigo, "detalhe": detalhe}
        if linha is not None:
            item["linha"] = linha
        achados.append(item)

    if not entrada.is_file():
        anotar("erro", "csv_ausente", "Arquivo evidencias.csv não encontrado")
        return {"linhas": 0, "erros": 1, "alertas": 0, "achados": achados}

    with entrada.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        campos = leitor.fieldnames or []
        faltantes = [campo for campo in CAMPOS if campo not in campos]
        if faltantes:
            anotar("erro", "colunas_ausentes", f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")
            return {"linhas": 0, "erros": 1, "alertas": 0, "achados": achados}
        registros = list(leitor)

    vistos: set[tuple[str, str, str, str]] = set()
    for numero, registro in enumerate(registros, start=2):
        dados = {campo: (registro.get(campo) or "").strip() for campo in CAMPOS}
        if None in registro:
            anotar("erro", "csv_malformado", "A linha possui mais campos que o cabeçalho", numero)
        try:
            date.fromisoformat(dados["data"])
        except ValueError:
            anotar("erro", "data_invalida", "A data deve seguir AAAA-MM-DD", numero)

        if dados["tipo"] not in TIPOS:
            anotar("erro", "tipo_invalido", f"Tipo não reconhecido: {dados['tipo']!r}", numero)
        if not dados["indicador"] or not dados["descricao"]:
            anotar("erro", "descricao_incompleta", "Indicador e descrição são obrigatórios", numero)
        if dados["tipo"] in {"quantitativa", "contagem"} and not dados["valor"]:
            anotar("erro", "valor_ausente", "Contagem sem valor informado", numero)
        if dados["tipo"] == "qualitativa" and not dados["quem_de_fora"]:
            anotar("alerta", "perfil_externo_ausente", "Registrar o perfil anônimo do participante, sem dados pessoais", numero)

        referencia = dados["arquivo"]
        if not referencia:
            anotar("erro", "referencia_ausente", "Falta caminho para arquivo de evidência", numero)
        else:
            rel = Path(referencia)
            alvo = (root / rel).resolve()
            if rel.is_absolute() or not alvo.is_relative_to(root / "evidencias"):
                anotar("erro", "caminho_inseguro", "A evidência deve ficar em evidencias/ e não sair do repositório", numero)
            elif not alvo.is_file():
                anotar("erro", "arquivo_ausente", f"Arquivo não existe: {referencia}", numero)
            elif alvo.stat().st_size == 0:
                anotar("erro", "arquivo_vazio", f"Arquivo vazio: {referencia}", numero)
            elif dados["tipo"] == "qualitativa" and alvo.suffix.lower() in {".md", ".txt"}:
                anotar("alerta", "registro_textual", f"{referencia}: texto da equipe não comprova sozinho teste externo; anexar resposta exportada, captura consentida ou outro registro primário verificável", numero)

        chave = (dados["data"], dados["tipo"], dados["indicador"], referencia)
        if chave in vistos:
            anotar("alerta", "registro_repetido", "Possível duplicação do mesmo indicador e arquivo", numero)
        vistos.add(chave)

    return {
        "linhas": len(registros),
        "erros": sum(x["nivel"] == "erro" for x in achados),
        "alertas": sum(x["nivel"] == "alerta" for x in achados),
        "achados": achados,
        "nota": "Auditoria documental, não autenticação de pessoas, respostas ou métricas; revisão humana é obrigatória.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--json", type=Path, help="Caminho opcional para salvar o relatório JSON")
    argumentos = parser.parse_args()
    resultado = auditar(argumentos.root)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    print(saida)
    if argumentos.json:
        argumentos.json.write_text(saida + "\n", encoding="utf-8")
    return 1 if resultado["erros"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
