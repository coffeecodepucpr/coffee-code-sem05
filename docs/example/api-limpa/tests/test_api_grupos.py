NOVO = {"nome_grupo": "Cálculo II na prática", "materia_id": 1, "max_participantes": 5}


def test_lista_os_seis_grupos(client):
    resposta = client.get("/grupos")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 6


def test_filtra_por_nome_e_por_materia(client):
    por_nome = client.get("/grupos", params={"q": "prática"}).json()
    assert [g["nome_grupo"] for g in por_nome] == ["Estruturas na prática"]
    por_materia = client.get("/grupos", params={"materia_id": 1}).json()
    assert [g["grupo_id"] for g in por_materia] == [1]


def test_busca_um_grupo(client):
    resposta = client.get("/grupos/3")
    assert resposta.status_code == 200
    assert resposta.json()["nome_grupo"] == "Modelagem e SQL"


def test_cria_um_grupo(client):
    resposta = client.post("/grupos", json=NOVO)
    assert resposta.status_code == 201
    assert resposta.headers["location"] == "/grupos/7"
    assert resposta.json()["grupo_id"] == 7


def test_put_substitui_o_grupo_inteiro(client):
    resposta = client.put("/grupos/1", json={"nome_grupo": "Cálculo revisado", "materia_id": 1})
    corpo = resposta.json()
    assert resposta.status_code == 200
    assert corpo["max_participantes"] == 10  # o PUT substitui tudo: voltou ao padrão
    assert corpo["criado_em"] == "2026-09-01T12:00:00Z"


def test_patch_altera_so_o_que_foi_enviado(client):
    corpo = client.patch("/grupos/3", json={"max_participantes": 12}).json()
    assert corpo["max_participantes"] == 12
    assert corpo["nome_grupo"] == "Modelagem e SQL"
    assert corpo["descricao"] == "Encontros online às terças e aos sábados"


def test_patch_aceita_null_so_na_descricao(client):
    resposta = client.patch("/grupos/3", json={"descricao": None})
    assert resposta.status_code == 200
    assert resposta.json()["descricao"] is None


def test_patch_com_null_nos_outros_campos_devolve_422_e_nao_corrompe(client):
    for campo in ("nome_grupo", "materia_id", "max_participantes"):
        resposta = client.patch("/grupos/1", json={campo: None})
        assert resposta.status_code == 422
        assert resposta.json()["detalhes"][0]["campo"] == f"body.{campo}"
    assert client.get("/grupos").status_code == 200  # a lista inteira continua saudável
    assert client.get("/grupos/1").json()["max_participantes"] == 6


def test_delete_devolve_204_sem_corpo_e_depois_404(client):
    resposta = client.delete("/grupos/2")
    assert resposta.status_code == 204
    assert resposta.content == b""
    assert client.delete("/grupos/2").status_code == 404
