"""O formato único de erro e o tratamento global."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.erros import registrar_tratadores


def test_erro_de_dominio_vira_404_com_o_formato_unico(client):
    resposta = client.get("/grupos/99")
    assert resposta.status_code == 404
    assert resposta.json() == {"erro": "grupo_nao_encontrado", "mensagem": "Grupo não encontrado", "detalhes": None}


def test_materia_inexistente_vira_422(client):
    resposta = client.post("/grupos", json={"nome_grupo": "Grupo fantasma", "materia_id": 99})
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "materia_inexistente"


def test_nome_repetido_vira_409(client):
    corpo = {"nome_grupo": "Cálculo II na prática", "materia_id": 1}
    client.post("/grupos", json=corpo)
    resposta = client.post("/grupos", json=corpo)
    assert resposta.status_code == 409
    assert resposta.json()["erro"] == "grupo_duplicado"


def test_erro_de_validacao_lista_cada_campo(client):
    resposta = client.post("/grupos", json={"nome_grupo": "ab", "materia_id": 0})
    corpo = resposta.json()
    assert resposta.status_code == 422
    assert corpo["erro"] == "validacao"
    assert [d["campo"] for d in corpo["detalhes"]] == ["body.nome_grupo", "body.materia_id"]


def test_identificador_que_nao_e_numero_aponta_o_caminho(client):
    corpo = client.get("/grupos/abc").json()
    assert corpo["detalhes"][0]["campo"] == "path.grupo_id"


def test_corpo_sem_content_type_devolve_422_no_formato_unico(client):
    resposta = client.post("/grupos", content='{"nome_grupo": "Sem cabecalho", "materia_id": 1}')
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "validacao"


def test_rota_inexistente_vira_404_no_formato_unico(client):
    resposta = client.get("/rota-que-nao-existe")
    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "nao_encontrado"


def test_metodo_nao_permitido_vira_405_e_mantem_o_cabecalho_allow(client):
    resposta = client.delete("/grupos")
    assert resposta.status_code == 405
    assert resposta.json()["erro"] == "metodo_nao_permitido"
    assert "allow" in resposta.headers


def test_erro_inesperado_vira_500_em_json_sem_vazar_detalhes():
    app_de_teste = FastAPI()
    registrar_tratadores(app_de_teste)

    @app_de_teste.get("/quebra")
    def quebra():
        raise RuntimeError("detalhe interno secreto")

    resposta = TestClient(app_de_teste, raise_server_exceptions=False).get("/quebra")
    assert resposta.status_code == 500
    assert resposta.json() == {"erro": "erro_interno", "mensagem": "Erro interno do servidor", "detalhes": None}
    assert "secreto" not in resposta.text
