from fastapi import APIRouter, HTTPException, status

from app import dados
from app.schemas import MateriaOut

router = APIRouter(prefix="/materias", tags=["materias"])


@router.get("", response_model=list[MateriaOut], summary="Lista as matérias")
def listar_materias():
    return list(dados.MATERIAS.values())


@router.get(
    "/{materia_id}",
    response_model=MateriaOut,
    summary="Busca uma matéria pelo identificador",
    responses={404: {"description": "Matéria não encontrada"}},
)
def buscar_materia(materia_id: int):
    materia = dados.MATERIAS.get(materia_id)
    if materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria não encontrada")
    return materia
