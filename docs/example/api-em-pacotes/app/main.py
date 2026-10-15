"""API Central do Buscador de Grupos de Estudo, dividida em pacotes e routers.

Rodar, na pasta api-em-pacotes:  fastapi dev app/main.py
"""
from fastapi import FastAPI

from app.routers import grupos, materias

DESCRICAO = """
API para cadastrar e consultar **grupos de estudo** e as **matérias** a que eles pertencem.

Os dados ficam **em memória**: ao reiniciar o servidor, tudo volta ao estado inicial.
"""

app = FastAPI(
    title="API Central: Buscador de Grupos de Estudo",
    description=DESCRICAO,
    version="1.1.0",
    openapi_tags=[
        {"name": "materias", "description": "Consulta das matérias (somente leitura)."},
        {"name": "grupos", "description": "CRUD completo dos grupos de estudo."},
    ],
)

app.include_router(materias.router)
app.include_router(grupos.router)


@app.get("/", include_in_schema=False)
def raiz():
    return {"api": "Buscador de Grupos de Estudo", "documentacao": "/docs"}
