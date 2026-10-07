#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

IGNORED = {"/", "/health", "/docs", "/redoc", "/openapi.json"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume consultas úteis da API para o evidencias.csv.")
    parser.add_argument("--log", default="logs/access.csv")
    args = parser.parse_args()
    path = Path(args.log)
    if not path.exists():
        raise SystemExit(f"Log não encontrado: {path}")

    useful = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["method"] == "GET" and row["path"] not in IGNORED and row["status"].startswith("2"):
                useful.append(row)

    by_path = Counter(row["path"] for row in useful)
    print(f"Consultas úteis bem-sucedidas: {len(useful)}")
    for path_name, count in by_path.most_common():
        print(f"{count:>5}  {path_name}")


if __name__ == "__main__":
    main()
