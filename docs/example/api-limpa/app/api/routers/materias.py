from fastapi import APIRouter

from app.api.dependencias import ServicoMateriasDep
from app.api.schemas import ErroOut, MateriaOut

router = APIRouter(
    prefix="/materias",
    tags=["materias"],
    responses={422: {"model": ErroOut, "description": "Dados inválidos (formato único de erro)"}},
)


@router.get("", response_model=list[MateriaOut], summary="Lista as matérias")
def listar_materias(servico: ServicoMateriasDep):
    return servico.listar()


@router.get(
    "/{materia_id}",
    response_model=MateriaOut,
    summary="Busca uma matéria pelo identificador",
    responses={404: {"model": ErroOut, "description": "Matéria não encontrada"}},
)
def buscar_materia(materia_id: int, servico: ServicoMateriasDep):
    return servico.buscar(materia_id)
