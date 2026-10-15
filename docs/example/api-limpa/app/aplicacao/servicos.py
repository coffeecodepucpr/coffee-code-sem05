"""Casos de uso: as regras da aplicação. Dependem só do domínio."""
from dataclasses import replace
from datetime import datetime, timezone

from app.dominio.entidades import Grupo, Materia
from app.dominio.erros import (
    GrupoDuplicadoError,
    GrupoNaoEncontradoError,
    MateriaInexistenteError,
    MateriaNaoEncontradaError,
)
from app.dominio.repositorios import RepositorioGrupos, RepositorioMaterias


class ServicoMaterias:
    def __init__(self, materias: RepositorioMaterias):
        self._materias = materias

    def listar(self) -> list[Materia]:
        return self._materias.listar()

    def buscar(self, materia_id: int) -> Materia:
        materia = self._materias.buscar(materia_id)
        if materia is None:
            raise MateriaNaoEncontradaError()
        return materia


class ServicoGrupos:
    def __init__(self, grupos: RepositorioGrupos, materias: RepositorioMaterias):
        self._grupos = grupos
        self._materias = materias

    # ---------- consultas
    def listar(
        self,
        q: str | None = None,
        materia_id: int | None = None,
        ordenar_por: str = "nome_grupo",
        ordem: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[Grupo], int]:
        """Devolve a página pedida e o total de grupos que atendem aos filtros."""
        grupos = self._grupos.listar()
        if q is not None:
            grupos = [g for g in grupos if q.lower() in g.nome_grupo.lower()]
        if materia_id is not None:
            grupos = [g for g in grupos if g.materia_id == materia_id]
        chave = (lambda g: g.nome_grupo.lower()) if ordenar_por == "nome_grupo" else (lambda g: getattr(g, ordenar_por))
        grupos.sort(key=chave, reverse=ordem == "desc")
        return grupos[offset : offset + limit], len(grupos)

    def buscar(self, grupo_id: int) -> Grupo:
        grupo = self._grupos.buscar(grupo_id)
        if grupo is None:
            raise GrupoNaoEncontradoError()
        return grupo

    # ---------- comandos
    def criar(self, nome_grupo: str, materia_id: int, max_participantes: int = 10, descricao: str | None = None) -> Grupo:
        self._conferir_materia(materia_id)
        self._conferir_nome_livre(nome_grupo, materia_id)
        novo = Grupo(None, nome_grupo, materia_id, max_participantes, descricao, datetime.now(timezone.utc))
        return self._grupos.salvar(novo)

    def substituir(self, grupo_id: int, nome_grupo: str, materia_id: int, max_participantes: int = 10, descricao: str | None = None) -> Grupo:
        antigo = self.buscar(grupo_id)
        self._conferir_materia(materia_id)
        self._conferir_nome_livre(nome_grupo, materia_id, ignorar_id=grupo_id)
        novo = Grupo(grupo_id, nome_grupo, materia_id, max_participantes, descricao, antigo.criado_em)
        return self._grupos.salvar(novo)

    def alterar(self, grupo_id: int, **campos) -> Grupo:
        antigo = self.buscar(grupo_id)
        novo = replace(antigo, **campos)  # um objeto NOVO: o antigo só é trocado se tudo der certo
        if "materia_id" in campos:
            self._conferir_materia(novo.materia_id)
        self._conferir_nome_livre(novo.nome_grupo, novo.materia_id, ignorar_id=grupo_id)
        return self._grupos.salvar(novo)

    def apagar(self, grupo_id: int) -> None:
        self.buscar(grupo_id)
        self._grupos.apagar(grupo_id)

    # ---------- regras internas
    def _conferir_materia(self, materia_id: int) -> None:
        if self._materias.buscar(materia_id) is None:
            raise MateriaInexistenteError(materia_id)

    def _conferir_nome_livre(self, nome_grupo: str, materia_id: int, ignorar_id: int | None = None) -> None:
        for g in self._grupos.listar():
            if g.nome_grupo.lower() == nome_grupo.lower() and g.materia_id == materia_id and g.grupo_id != ignorar_id:
                raise GrupoDuplicadoError()
