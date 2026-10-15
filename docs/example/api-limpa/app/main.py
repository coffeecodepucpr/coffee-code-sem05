"""API Central do Buscador de Grupos de Estudo, com Clean Architecture.

Rodar, na pasta api-limpa:  fastapi dev app/main.py
"""
from fastapi import FastAPI

from app.api.erros import registrar_tratadores
from app.api.routers import grupos, materias

DESCRICAO = """
API para cadastrar e consultar **grupos de estudo** e as **matérias** a que eles pertencem.

Todos os erros seguem o mesmo formato: `erro`, `mensagem` e, quando houver, `detalhes`.

Os dados ficam **em memória**: ao reiniciar o servidor, tudo volta ao estado inicial.
"""

app = FastAPI(
    title="API Central: Buscador de Grupos de Estudo",
    description=DESCRICAO,
    version="2.0.0",
    openapi_tags=[
        {"name": "materias", "description": "Consulta das matérias (somente leitura)."},
        {"name": "grupos", "description": "CRUD completo dos grupos, com filtros e paginação."},
    ],
)

registrar_tratadores(app)
app.include_router(materias.router)
app.include_router(grupos.router)


@app.get("/", include_in_schema=False)
def raiz():
    return {"api": "Buscador de Grupos de Estudo", "documentacao": "/docs"}
