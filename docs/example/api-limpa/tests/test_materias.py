def test_lista_as_seis_materias(client):
    assert len(client.get("/materias").json()) == 6


def test_busca_uma_materia(client):
    assert client.get("/materias/1").json() == {"materia_id": 1, "nome": "Cálculo I", "codigo": "MAT101"}


def test_materia_inexistente_devolve_404(client):
    resposta = client.get("/materias/99")
    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "materia_nao_encontrada"
