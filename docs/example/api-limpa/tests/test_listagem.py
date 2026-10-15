def test_pagina_o_resultado_e_informa_o_total(client):
    resposta = client.get("/grupos", params={"limit": 2, "offset": 2})
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2
    assert resposta.headers["x-total-count"] == "6"


def test_ordena_por_limite_em_ordem_decrescente(client):
    grupos = client.get("/grupos", params={"ordenar_por": "max_participantes", "ordem": "desc"}).json()
    limites = [g["max_participantes"] for g in grupos]
    assert limites == sorted(limites, reverse=True)
    assert grupos[0]["nome_grupo"] == "Modelagem e SQL"


def test_ordena_por_nome_por_padrao(client):
    nomes = [g["nome_grupo"] for g in client.get("/grupos").json()]
    assert nomes == sorted(nomes, key=str.lower)


def test_total_conta_depois_do_filtro_e_antes_da_pagina(client):
    resposta = client.get("/grupos", params={"q": "prática", "limit": 1})
    assert resposta.headers["x-total-count"] == "1"


def test_limites_invalidos_devolvem_422(client):
    for params in ({"limit": 0}, {"limit": 101}, {"offset": -1}, {"ordenar_por": "inexistente"}):
        assert client.get("/grupos", params=params).status_code == 422
