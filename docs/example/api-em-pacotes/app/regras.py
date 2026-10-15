"""Regras de negócio reutilizadas pelas rotas."""
from fastapi import HTTPException, status

from app import dados


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
