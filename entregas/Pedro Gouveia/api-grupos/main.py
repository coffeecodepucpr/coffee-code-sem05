from fastapi import FastAPI, HTTPException, Response, status
import dados
from schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate, MateriaOut
from datetime import datetime, timezone

app = FastAPI(
	title= "API Buscador de Grupos",
	description= "Uma API usada para encontrar grupos de estudo para uma dada matéria, ou manipular dados",
	version= "1.0.0"
)

def materia_existe(materia_id) -> None:
	if materia_id not in dados.materias:
		raise HTTPException(
			status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
			detail= f"A materia {materia_id} não existe"
		)

def conflito_de_nome(grupo_nome: str, materia_id: int, ignorar_id: int | None = None) -> None:
	for grupo in dados.grupos.values():
		mesmo_nome= grupo["grupo_nome"].lower() == grupo_nome.lower()
		if mesmo_nome and grupo["materia_id"] == materia_id and grupo["grupo_id"] != ignorar_id:
			raise HTTPException(
				status_code= status.HTTP_409_CONFLICT,
				detail= "Já existe um grupo com esse nome na matéria escolhida"
			)

def grupo_ou_404(grupo_id: int) -> dict:
	grupo = dados.grupos.get(grupo_id)
	if grupo is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
	return grupo


@app.get("/materias", response_model=list[MateriaOut],
	summary= "Mostra uma lista completa com todas as matérias")
def listar_materias():
	return list(dados.materias.values())


@app.get("/materias/{materia_id}", response_model=MateriaOut,
	summary= "Busca uma matéria especificada pelo ID de matéria na URL",
	responses= {
		404: {"description": "Matéria não encontrada"},
		422: {"description": "Valor inserido inválido"}})
def buscar_materia(materia_id: int):
	materia= dados.materias.get(materia_id)
	if materia is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria não encontrada")
	return materia

@app.get("/grupos/{grupo_id}", response_model=GrupoOut,
	summary= "Busca por um grupo específico pelo ID do grupo na URL",
	responses= {
		404: {"description": "Grupo não encontrado"},
		422: {"description": "Valor inserido inválido"}})
def buscar_grupo(grupo_id: int):
	return grupo_ou_404(grupo_id)

@app.get("/grupos", response_model=list[GrupoOut],
	summary= "Mostra uma lista completa de todas os grupos",
	responses= {
		422: {"description": "Valor inserido inválido"}})
def listar_grupo(q: str | None = None, materia_id: int | None = None):
	grupos = list(dados.grupos.values())
	if q is not None:
		grupos = [g for g in grupos if q.lower() in g["grupo_nome"].lower()]
	if materia_id is not None:
		grupos = [g for g in grupos if g["materia_id"] == materia_id]
	return grupos


@app.post("/grupos", response_model=GrupoOut, status_code=status.HTTP_201_CREATED,
	summary= "Cria um grupo com base no modelo GrupoCreate",
	responses= {
		409: {"description": "Valores inseridos entram em conflito com outros já registrados"},
		422: {"description": "Valor inserido inválido"}})
def criar_grupo(novo: GrupoCreate, response: Response):
	materia_existe(novo.materia_id)
	conflito_de_nome(novo.grupo_nome, novo.materia_id)
	grupo_id = next(dados.contador_grupos)
	grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": datetime.now(timezone.utc)}
	dados.grupos[grupo_id] = grupo
	response.headers["Location"] = f"/grupos/{grupo_id}"
	return grupo

@app.put("/grupos/{grupo_id}", response_model=GrupoOut,
	summary= "Seleciona um grupo pelo seu ID e substitui todos seus valores, mantendo valores padrões caso não informado",
	responses= {
		404: {"description": "Grupo não encontrado"},
		409: {"description": "Valores inseridos entram em conflito com outros já registrados"},
		422: {"description": "Valor inserido inválido"}})
def trocar_grupo(grupo_id: int, novo: GrupoUpdate):
	antigo= grupo_ou_404(grupo_id)
	materia_existe(novo.materia_id)
	conflito_de_nome(novo.grupo_nome, novo.materia_id, ignorar_id= grupo_id)
	grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": antigo["criado_em"]}
	dados.grupos[grupo_id] = grupo
	return grupo

@app.patch("/grupos/{grupo_id}", response_model= GrupoOut,
	summary= "Seleciona um grupo pelo seu ID e modifica seus valores com base nos campos informados, permitindo alterar um sem mexer nos outros",
	responses= {
		404: {"description": "Grupo não encontrado"},
		409: {"description": "Valores inseridos entram em conflito com outros já registrados"},
		422: {"description": "Valor inserido inválido"}})
def modificar_grupo(grupo_id: int, mudancas: GrupoPatch):
	grupo= grupo_ou_404(grupo_id)
	campos= mudancas.model_dump(exclude_unset=True)
	if "materia_id" in campos:
		materia_existe(campos["materia_id"])
	nome= campos.get("grupo_nome", grupo["grupo_nome"])
	materia= campos.get("materia_id", grupo["materia_id"])
	conflito_de_nome(nome, materia, ignorar_id= grupo_id)
	grupo.update(campos)
	return grupo

@app.delete("/grupos/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT,
	summary= "Exclui o grupo com o ID informado na URL",
	responses= {
		404: {"description": "Grupo não encontrado"},
		422: {"description": "Valor inserido inválido"}})
def excluir_grupo(grupo_id: int):
	grupo_ou_404(grupo_id)
	del dados.grupos[grupo_id]

























