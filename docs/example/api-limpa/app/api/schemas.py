"""Modelos Pydantic: o formato dos dados na borda HTTP."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MateriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    materia_id: int
    nome: str
    codigo: str


class GrupoBase(BaseModel):
    nome_grupo: str = Field(min_length=3, max_length=60, description="Nome do grupo de estudo")
    materia_id: int = Field(gt=0, description="Identificador da matéria do grupo")
    max_participantes: int = Field(default=10, ge=2, le=50, description="Limite de participantes")
    descricao: str | None = Field(default=None, max_length=200, description="Texto livre, opcional")


class GrupoCreate(GrupoBase):
    """Corpo do POST."""


class GrupoUpdate(GrupoBase):
    """Corpo do PUT: substitui o grupo inteiro."""


class GrupoPatch(BaseModel):
    """Corpo do PATCH: omitir um campo significa não alterá-lo. Só a descrição aceita null."""

    nome_grupo: str | None = Field(default=None, min_length=3, max_length=60)
    materia_id: int | None = Field(default=None, gt=0)
    max_participantes: int | None = Field(default=None, ge=2, le=50)
    descricao: str | None = Field(default=None, max_length=200)

    @field_validator("nome_grupo", "materia_id", "max_participantes")
    @classmethod
    def nao_aceita_null(cls, valor):
        if valor is None:
            raise ValueError("este campo não aceita null: omita-o para não alterá-lo")
        return valor


class GrupoOut(GrupoBase):
    model_config = ConfigDict(from_attributes=True)

    grupo_id: int
    criado_em: datetime


class DetalheErro(BaseModel):
    campo: str
    mensagem: str


class ErroOut(BaseModel):
    """O formato único de erro da API."""

    erro: str
    mensagem: str
    detalhes: list[DetalheErro] | None = None
