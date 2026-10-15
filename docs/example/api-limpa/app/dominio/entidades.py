"""Entidades do domínio: os conceitos do sistema, sem nenhuma tecnologia."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Materia:
    materia_id: int
    nome: str
    codigo: str


@dataclass
class Grupo:
    grupo_id: int | None  # None enquanto o grupo ainda não foi guardado
    nome_grupo: str
    materia_id: int
    max_participantes: int
    descricao: str | None
    criado_em: datetime
