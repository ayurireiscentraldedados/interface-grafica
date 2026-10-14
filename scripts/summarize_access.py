#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

IGNORED = {"/", "/health", "/docs", "/redoc", "/openapi.json"}
RENDER_LINE = re.compile(r"ACESSO (\S+) (\S+) (\S+) (\d{3}) (\S+)")


def read_csv_log(path: Path) -> list[tuple]:
    with path.open(encoding="utf-8") as handle:
        return [
            (r["timestamp_utc"], r["method"], r["path"], r["status"], r["duration_ms"])
            for r in csv.DictReader(handle)
        ]


def read_render_log(path: Path) -> list[tuple]:
    rows = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = RENDER_LINE.search(line)
            if match:
                rows.append(match.groups())
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume consultas úteis da API para o evidencias.csv.")
    parser.add_argument("--log", action="append", default=[], help="CSV de acessos (logs/access.csv). Pode repetir.")
    parser.add_argument(
        "--render-log",
        action="append",
        default=[],
        help="Texto copiado dos logs do Render, com linhas 'ACESSO ...'. Pode repetir.",
    )
    args = parser.parse_args()

    sources = [(Path(p), read_csv_log) for p in args.log] + [(Path(p), read_render_log) for p in args.render_log]
    if not sources:
        sources = [(Path("logs/access.csv"), read_csv_log)]

    # Juntar fontes sobrepostas não conta o mesmo acesso duas vezes.
    unique: set[tuple] = set()
    for path, reader in sources:
        if not path.exists():
            raise SystemExit(f"Log não encontrado: {path}")
        unique.update(reader(path))

    useful = sorted(
        row for row in unique
        if row[1] == "GET" and row[2] not in IGNORED and row[3].startswith("2")
    )
    by_path = Counter(row[2] for row in useful)
    print(f"Consultas úteis bem-sucedidas: {len(useful)}")
    if useful:
        print(f"Período observado (UTC): {useful[0][0][:19]} até {useful[-1][0][:19]}")
    for path_name, count in by_path.most_common():
        print(f"{count:>5}  {path_name}")


if __name__ == "__main__":
    main()
