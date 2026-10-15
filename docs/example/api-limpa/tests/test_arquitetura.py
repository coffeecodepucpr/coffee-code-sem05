"""A regra da dependência, verificada por um teste.

Se alguém importar o FastAPI dentro do núcleo, este teste falha.
"""
import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "app"
PROIBIDOS_NO_NUCLEO = ("fastapi", "starlette", "pydantic", "app.api", "app.infraestrutura")
PROIBIDOS_NA_INFRA = ("fastapi", "starlette", "app.api")


def _importacoes(pasta: str) -> set[str]:
    nomes = set()
    for arquivo in (RAIZ / pasta).glob("*.py"):
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            if isinstance(no, ast.Import):
                nomes.update(alias.name for alias in no.names)
            elif isinstance(no, ast.ImportFrom) and no.module:
                nomes.add(no.module)
    return nomes


def _proibidos(importados: set[str], proibidos: tuple[str, ...]) -> list[str]:
    return sorted(n for n in importados if any(n == p or n.startswith(p + ".") for p in proibidos))


def test_dominio_nao_importa_framework_nem_outras_camadas():
    assert _proibidos(_importacoes("dominio"), PROIBIDOS_NO_NUCLEO + ("app.aplicacao",)) == []


def test_aplicacao_nao_importa_framework_nem_api_nem_infraestrutura():
    assert _proibidos(_importacoes("aplicacao"), PROIBIDOS_NO_NUCLEO) == []


def test_infraestrutura_nao_importa_framework_nem_api():
    assert _proibidos(_importacoes("infraestrutura"), PROIBIDOS_NA_INFRA) == []
