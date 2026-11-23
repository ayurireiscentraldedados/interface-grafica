"""Registra a página /explorar sem reescrever as rotas e os arquivos dos colegas.

Execute na raiz do repositório depois de extrair o pacote. Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app" / "main.py"
README = ROOT / "README.md"

import_line = "from app.explorer import router as explorer_router\n"
anchor = "from app.routes import router\n"
include_line = "app.include_router(explorer_router)\n"

source = MAIN.read_text(encoding="utf-8")
if import_line not in source:
    if source.count(anchor) != 1:
        raise SystemExit("Não encontrei o ponto de importação em app/main.py; nenhuma alteração feita.")
    source = source.replace(anchor, anchor + import_line)

if include_line not in source:
    insertion = "app.include_router(router)"
    if source.count(insertion) != 1:
        raise SystemExit("Não encontrei o registro do router; nenhuma alteração feita.")
    source = source.replace(insertion, insertion + "\n" + include_line.rstrip("\n"))

MAIN.write_text(source, encoding="utf-8")

text = README.read_text(encoding="utf-8")
intro = """## Para quem não programa: consulta guiada

Acesse **`/explorar`** na API pública para pesquisar acidentes por município,
ver as rodovias com mais registros e identificar trechos de 10 km.
A página funciona em celular ou computador, sem cadastro, código IBGE,
comandos de terminal ou conhecimento de JSON.

- Interface pública (após o deploy): https://api-seguranca-viaria-ce.onrender.com/explorar
- API técnica e documentação Swagger: https://api-seguranca-viaria-ce.onrender.com/docs
- O ano de 2026 está disponível apenas até 31/08/2026 no pacote atualmente publicado.
- O recorte cobre acidentes registrados pela PRF em rodovias federais; maiores
  contagens não significam necessariamente maior risco.
- A interface usa as rotas JSON já existentes; ela não cria dados novos.

"""
if "## Para quem não programa: consulta guiada" not in text:
    anchor_readme = "## Como usar agora\n"
    if text.count(anchor_readme) != 1:
        raise SystemExit("Não encontrei ponto seguro para inserir seção no README.")
    text = text.replace(anchor_readme, intro + anchor_readme)
    README.write_text(text, encoding="utf-8")

print("Página /explorar registrada no FastAPI; README atualizado.")
