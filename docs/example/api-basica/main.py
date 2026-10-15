"""API Central do Buscador de Grupos de Estudo (Parte 1: CRUD).

Rodar:  fastapi dev main.py
Docs:   http://127.0.0.1:8000/docs
"""
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status

import dados
from schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate, MateriaOut

DESCRICAO = """
API para cadastrar e consultar **grupos de estudo** e as **matérias** a que eles pertencem.

Os dados ficam **em memória**: ao reiniciar o servidor, tudo volta ao estado inicial.
"""

app = FastAPI(
    title="API Central: Buscador de Grupos de Estudo",
    description=DESCRICAO,
    version="1.0.0",
    openapi_tags=[
        {"name": "materias", "description": "Consulta das matérias (somente leitura)."},
        {"name": "grupos", "description": "CRUD completo dos grupos de estudo."},
    ],
)


# ---------- funções de apoio ----------

def buscar_grupo_ou_404(grupo_id: int) -> dict:
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
    return grupo


def conferir_materia(materia_id: int) -> None:
    if materia_id not in dados.MATERIAS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"A matéria {materia_id} não existe",
        )


def conferir_nome_livre(nome_grupo: str, materia_id: int, ignorar_id: int | None = None) -> None:
    for grupo in dados.GRUPOS.values():
        mesmo_nome = grupo["nome_grupo"].lower() == nome_grupo.lower()
        if mesmo_nome and grupo["materia_id"] == materia_id and grupo["grupo_id"] != ignorar_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um grupo com esse nome nessa matéria",
            )


# ---------- raiz ----------

@app.get("/", include_in_schema=False)
def raiz():
    return {"api": "Buscador de Grupos de Estudo", "documentacao": "/docs"}


# ---------- matérias (somente leitura) ----------

@app.get("/materias", response_model=list[MateriaOut], tags=["materias"], summary="Lista as matérias")
def listar_materias():
    return list(dados.MATERIAS.values())


@app.get(
    "/materias/{materia_id}",
    response_model=MateriaOut,
    tags=["materias"],
    summary="Busca uma matéria pelo identificador",
    responses={404: {"description": "Matéria não encontrada"}},
)
def buscar_materia(materia_id: int):
    materia = dados.MATERIAS.get(materia_id)
    if materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria não encontrada")
    return materia


# ---------- grupos (CRUD) ----------

@app.get("/grupos", response_model=list[GrupoOut], tags=["grupos"], summary="Lista os grupos")
def listar_grupos(q: str | None = None, materia_id: int | None = None):
    grupos = list(dados.GRUPOS.values())
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g["nome_grupo"].lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g["materia_id"] == materia_id]
    return grupos


@app.get(
    "/grupos/{grupo_id}",
    response_model=GrupoOut,
    tags=["grupos"],
    summary="Busca um grupo pelo identificador",
    responses={404: {"description": "Grupo não encontrado"}},
)
def buscar_grupo(grupo_id: int):
    return buscar_grupo_ou_404(grupo_id)


@app.post(
    "/grupos",
    response_model=GrupoOut,
    status_code=status.HTTP_201_CREATED,
    tags=["grupos"],
    summary="Cria um grupo",
    responses={
        409: {"description": "Já existe um grupo com esse nome nessa matéria"},
        422: {"description": "Dados inválidos, ou matéria inexistente"},
    },
)
def criar_grupo(novo: GrupoCreate, response: Response):
    conferir_materia(novo.materia_id)
    conferir_nome_livre(novo.nome_grupo, novo.materia_id)
    grupo_id = next(dados.CONTADOR_GRUPOS)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": datetime.now(timezone.utc)}
    dados.GRUPOS[grupo_id] = grupo
    response.headers["Location"] = f"/grupos/{grupo_id}"
    return grupo


@app.put(
    "/grupos/{grupo_id}",
    response_model=GrupoOut,
    tags=["grupos"],
    summary="Substitui um grupo inteiro",
    responses={404: {"description": "Grupo não encontrado"}, 409: {"description": "Nome já usado nessa matéria"}},
)
def substituir_grupo(grupo_id: int, novo: GrupoUpdate):
    antigo = buscar_grupo_ou_404(grupo_id)
    conferir_materia(novo.materia_id)
    conferir_nome_livre(novo.nome_grupo, novo.materia_id, ignorar_id=grupo_id)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": antigo["criado_em"]}
    dados.GRUPOS[grupo_id] = grupo
    return grupo


@app.patch(
    "/grupos/{grupo_id}",
    response_model=GrupoOut,
    tags=["grupos"],
    summary="Altera só alguns campos de um grupo",
    responses={404: {"description": "Grupo não encontrado"}, 409: {"description": "Nome já usado nessa matéria"}},
)
def alterar_grupo(grupo_id: int, mudancas: GrupoPatch):
    grupo = buscar_grupo_ou_404(grupo_id)
    campos = mudancas.model_dump(exclude_unset=True)
    if "materia_id" in campos:
        conferir_materia(campos["materia_id"])
    nome = campos.get("nome_grupo", grupo["nome_grupo"])
    materia = campos.get("materia_id", grupo["materia_id"])
    conferir_nome_livre(nome, materia, ignorar_id=grupo_id)
    grupo.update(campos)
    return grupo


@app.delete(
    "/grupos/{grupo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["grupos"],
    summary="Apaga um grupo",
    responses={404: {"description": "Grupo não encontrado"}},
)
def apagar_grupo(grupo_id: int):
    buscar_grupo_ou_404(grupo_id)
    del dados.GRUPOS[grupo_id]
