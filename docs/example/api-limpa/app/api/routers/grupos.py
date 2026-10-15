from fastapi import APIRouter, Response, status

from app.api.dependencias import Ordenacao, Paginacao, ServicoGruposDep
from app.api.schemas import ErroOut, GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate

router = APIRouter(
    prefix="/grupos",
    tags=["grupos"],
    responses={422: {"model": ErroOut, "description": "Dados inválidos (formato único de erro)"}},
)

NAO_ENCONTRADO = {"model": ErroOut, "description": "Grupo não encontrado"}
CONFLITO = {"model": ErroOut, "description": "Já existe um grupo com esse nome nessa matéria"}


@router.get("", response_model=list[GrupoOut], summary="Lista os grupos")
def listar_grupos(
    response: Response,
    servico: ServicoGruposDep,
    paginacao: Paginacao,
    ordenacao: Ordenacao,
    q: str | None = None,
    materia_id: int | None = None,
):
    grupos, total = servico.listar(
        q=q, materia_id=materia_id, ordenar_por=ordenacao["ordenar_por"], ordem=ordenacao["ordem"],
        limit=paginacao["limit"], offset=paginacao["offset"],
    )
    response.headers["X-Total-Count"] = str(total)
    return grupos


@router.get("/{grupo_id}", response_model=GrupoOut, summary="Busca um grupo pelo identificador", responses={404: NAO_ENCONTRADO})
def buscar_grupo(grupo_id: int, servico: ServicoGruposDep):
    return servico.buscar(grupo_id)


@router.post("", response_model=GrupoOut, status_code=status.HTTP_201_CREATED, summary="Cria um grupo", responses={409: CONFLITO})
def criar_grupo(novo: GrupoCreate, response: Response, servico: ServicoGruposDep):
    grupo = servico.criar(**novo.model_dump())
    response.headers["Location"] = f"/grupos/{grupo.grupo_id}"
    return grupo


@router.put("/{grupo_id}", response_model=GrupoOut, summary="Substitui um grupo inteiro", responses={404: NAO_ENCONTRADO, 409: CONFLITO})
def substituir_grupo(grupo_id: int, novo: GrupoUpdate, servico: ServicoGruposDep):
    return servico.substituir(grupo_id, **novo.model_dump())


@router.patch("/{grupo_id}", response_model=GrupoOut, summary="Altera só alguns campos de um grupo", responses={404: NAO_ENCONTRADO, 409: CONFLITO})
def alterar_grupo(grupo_id: int, mudancas: GrupoPatch, servico: ServicoGruposDep):
    return servico.alterar(grupo_id, **mudancas.model_dump(exclude_unset=True))


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Apaga um grupo", responses={404: NAO_ENCONTRADO})
def apagar_grupo(grupo_id: int, servico: ServicoGruposDep):
    servico.apagar(grupo_id)
