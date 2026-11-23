"""Página pública de consultas guiadas para pessoas sem conhecimento de APIs.

Não altera as rotas JSON existentes. A interface consome os mesmos endpoints
que já alimentam clientes externos e evita bibliotecas de frontend adicionais.
"""
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)
_PAGE = Path(__file__).resolve().parent / "static" / "explorar.html"


@router.get("/explorar", response_class=HTMLResponse)
def explorar() -> HTMLResponse:
    return HTMLResponse(
        _PAGE.read_text(encoding="utf-8"),
        headers={
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
        },
    )
