from datetime import datetime, timezone

from fastapi import APIRouter, Response, status

from app import dados, regras
from app.schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate

router = APIRouter(prefix="/grupos", tags=["grupos"])


@router.get("", response_model=list[GrupoOut], summary="Lista os grupos")
def listar_grupos(q: str | None = None, materia_id: int | None = None):
    grupos = list(dados.GRUPOS.values())
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g["nome_grupo"].lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g["materia_id"] == materia_id]
    return grupos


@router.get(
    "/{grupo_id}",
    response_model=GrupoOut,
    summary="Busca um grupo pelo identificador",
    responses={404: {"description": "Grupo não encontrado"}},
)
def buscar_grupo(grupo_id: int):
    return regras.buscar_grupo_ou_404(grupo_id)


@router.post(
    "",
    response_model=GrupoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um grupo",
    responses={
        409: {"description": "Já existe um grupo com esse nome nessa matéria"},
        422: {"description": "Dados inválidos, ou matéria inexistente"},
    },
)
def criar_grupo(novo: GrupoCreate, response: Response):
    regras.conferir_materia(novo.materia_id)
    regras.conferir_nome_livre(novo.nome_grupo, novo.materia_id)
    grupo_id = next(dados.CONTADOR_GRUPOS)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": datetime.now(timezone.utc)}
    dados.GRUPOS[grupo_id] = grupo
    response.headers["Location"] = f"/grupos/{grupo_id}"
    return grupo


@router.put(
    "/{grupo_id}",
    response_model=GrupoOut,
    summary="Substitui um grupo inteiro",
    responses={404: {"description": "Grupo não encontrado"}, 409: {"description": "Nome já usado nessa matéria"}},
)
def substituir_grupo(grupo_id: int, novo: GrupoUpdate):
    antigo = regras.buscar_grupo_ou_404(grupo_id)
    regras.conferir_materia(novo.materia_id)
    regras.conferir_nome_livre(novo.nome_grupo, novo.materia_id, ignorar_id=grupo_id)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": antigo["criado_em"]}
    dados.GRUPOS[grupo_id] = grupo
    return grupo


@router.patch(
    "/{grupo_id}",
    response_model=GrupoOut,
    summary="Altera só alguns campos de um grupo",
    responses={404: {"description": "Grupo não encontrado"}, 409: {"description": "Nome já usado nessa matéria"}},
)
def alterar_grupo(grupo_id: int, mudancas: GrupoPatch):
    grupo = regras.buscar_grupo_ou_404(grupo_id)
    campos = mudancas.model_dump(exclude_unset=True)
    if "materia_id" in campos:
        regras.conferir_materia(campos["materia_id"])
    nome = campos.get("nome_grupo", grupo["nome_grupo"])
    materia = campos.get("materia_id", grupo["materia_id"])
    regras.conferir_nome_livre(nome, materia, ignorar_id=grupo_id)
    grupo.update(campos)
    return grupo


@router.delete(
    "/{grupo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Apaga um grupo",
    responses={404: {"description": "Grupo não encontrado"}},
)
def apagar_grupo(grupo_id: int):
    regras.buscar_grupo_ou_404(grupo_id)
    del dados.GRUPOS[grupo_id]
