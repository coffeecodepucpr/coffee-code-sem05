from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class GrupoBase(BaseModel):
	grupo_nome: str = Field(min_length=3, max_length=60)
	materia_id: int = Field(gt=0)
	max_participantes: int = Field(default=15, ge=2, le=50)

class GrupoUpdate(GrupoBase):
	"""corpo"""

class GrupoCreate(GrupoBase):
	"""corpo"""

class GrupoOut(GrupoBase):
	grupo_id: int
	criado_em: datetime

class GrupoPatch(BaseModel):
	nome_grupo: str | None = Field(default=None, min_length=3, max_length=60)
	materia_id: int | None = Field(default=None, gt=0)
	max_participantes: int | None = Field(default=None, ge=2, le=50)

	@field_validator("nome_grupo", "materia_id", "max_participantes")
	@classmethod
	def nao_aceita_null(cls, valor):
		if valor is None:
			raise ValueError("este campo não aceita null: omita-o para não alterá-lo")
		return valor

class MateriaOut(BaseModel):
	nome: str 
	materia_id: int 
	codigo: str 
