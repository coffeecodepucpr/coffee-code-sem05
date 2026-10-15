"""Repositórios que guardam os dados em memória (implementam as interfaces do domínio)."""
import itertools
from dataclasses import replace
from datetime import datetime, timezone

from app.dominio.entidades import Grupo, Materia


def _data(dia: int) -> datetime:
    return datetime(2026, 9, dia, 12, 0, tzinfo=timezone.utc)


class RepositorioMateriasEmMemoria:
    def __init__(self, materias: list[Materia]):
        self._materias = {m.materia_id: m for m in materias}

    def listar(self) -> list[Materia]:
        return list(self._materias.values())

    def buscar(self, materia_id: int) -> Materia | None:
        return self._materias.get(materia_id)


class RepositorioGruposEmMemoria:
    def __init__(self, grupos: list[Grupo]):
        self._grupos = {g.grupo_id: g for g in grupos}
        self._contador = itertools.count(max(self._grupos, default=0) + 1)

    def listar(self) -> list[Grupo]:
        return list(self._grupos.values())

    def buscar(self, grupo_id: int) -> Grupo | None:
        return self._grupos.get(grupo_id)

    def salvar(self, grupo: Grupo) -> Grupo:
        if grupo.grupo_id is None:
            grupo = replace(grupo, grupo_id=next(self._contador))
        self._grupos[grupo.grupo_id] = grupo
        return grupo

    def apagar(self, grupo_id: int) -> None:
        del self._grupos[grupo_id]


def novo_repositorio_de_materias() -> RepositorioMateriasEmMemoria:
    return RepositorioMateriasEmMemoria([
        Materia(1, "Cálculo I", "MAT101"),
        Materia(2, "Estrutura de Dados", "INF201"),
        Materia(3, "Banco de Dados", "INF301"),
        Materia(4, "Engenharia de Software", "INF305"),
        Materia(5, "Redes de Computadores", "INF310"),
        Materia(6, "Sistemas Operacionais", "INF315"),
    ])


def novo_repositorio_de_grupos() -> RepositorioGruposEmMemoria:
    return RepositorioGruposEmMemoria([
        Grupo(1, "Cálculo passo a passo", 1, 6, None, _data(1)),
        Grupo(2, "Estruturas na prática", 2, 5, None, _data(2)),
        Grupo(3, "Modelagem e SQL", 3, 8, "Encontros online às terças e aos sábados", _data(3)),
        Grupo(4, "Requisitos e histórias", 4, 5, None, _data(4)),
        Grupo(5, "Redes na unha", 5, 6, None, _data(5)),
        Grupo(6, "Processos e memória", 6, 4, None, _data(6)),
    ])
