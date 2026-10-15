"""Interfaces dos repositórios: o que o núcleo PRECISA, sem dizer COMO é feito.

Quem guarda os dados de verdade (memória, banco, arquivo) implementa estas
interfaces. O núcleo só conhece as interfaces.
"""
from typing import Protocol

from app.dominio.entidades import Grupo, Materia


class RepositorioMaterias(Protocol):
    def listar(self) -> list[Materia]: ...

    def buscar(self, materia_id: int) -> Materia | None: ...


class RepositorioGrupos(Protocol):
    def listar(self) -> list[Grupo]: ...

    def buscar(self, grupo_id: int) -> Grupo | None: ...

    def salvar(self, grupo: Grupo) -> Grupo:
        """Guarda o grupo. Se ele ainda não tem identificador, cria um."""
        ...

    def apagar(self, grupo_id: int) -> None: ...
