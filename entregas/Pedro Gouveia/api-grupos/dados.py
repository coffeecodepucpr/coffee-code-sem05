import itertools
from datetime import datetime, timezone

materias = {1:{"materia_id":1,"nome":"Engenharia de Software","codigo":"ENGSOFT101"},
	2:{"materia_id":2,"nome":"Jogos Digitais","codigo":"JOGOS203"},
	3:{"materia_id":3,"nome":"Biomecânica","codigo":"BIOMEC304"},
	4:{"materia_id":4,"nome":"Educação Física","codigo":"EDF707"},
	5:{"materia_id":5,"nome":"Astronomia","codigo":"AST901"},
	6:{"materia_id":6,"nome":"Engenharia Civil","codigo":"ECV802"}}

def _data(dia: int):
	return datetime(2026, 10, dia, 12, 0, tzinfo=timezone.utc)

grupos = {1:{"grupo_id":1,"grupo_nome":"Software 2","materia_id":1,"criado_em":_data(1),"max_participantes":15},
	2:{"grupo_id":2,"grupo_nome":"Jogos 3","materia_id":2,"criado_em":_data(1),"max_participantes":15},
	3:{"grupo_id":3,"grupo_nome":"Biomecânica 7","materia_id":3,"criado_em":_data(1),"max_participantes":15},
	4:{"grupo_id":4,"grupo_nome":"Ed Física 2","materia_id":4,"criado_em":_data(2),"max_participantes":15},
	5:{"grupo_id":5,"grupo_nome":"Astro 1","materia_id":5,"criado_em":_data(2),"max_participantes":15},
	6:{"grupo_id":6,"grupo_nome":"EnCiv 3","materia_id":6,"criado_em":_data(2),"max_participantes":15}}

contador_grupos= itertools.count(7)