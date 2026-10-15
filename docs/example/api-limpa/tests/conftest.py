import pytest
from fastapi.testclient import TestClient

from app.api import dependencias
from app.aplicacao.servicos import ServicoGrupos, ServicoMaterias
from app.infraestrutura.memoria import novo_repositorio_de_grupos, novo_repositorio_de_materias
from app.main import app


@pytest.fixture
def servicos():
    """Os casos de uso, com repositórios novos em memória: sem HTTP, sem FastAPI."""
    materias = novo_repositorio_de_materias()
    grupos = novo_repositorio_de_grupos()
    return ServicoGrupos(grupos, materias), ServicoMaterias(materias)


@pytest.fixture
def client(servicos):
    """Um cliente HTTP cujos serviços foram trocados por versões com dados limpos."""
    servico_grupos, servico_materias = servicos
    app.dependency_overrides[dependencias.obter_servico_grupos] = lambda: servico_grupos
    app.dependency_overrides[dependencias.obter_servico_materias] = lambda: servico_materias
    yield TestClient(app)
    app.dependency_overrides.clear()
