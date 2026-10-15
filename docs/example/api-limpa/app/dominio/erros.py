"""Erros do domínio: dizem o que deu errado nas regras, sem falar de HTTP.

Repare que nenhum deles menciona código de status, JSON ou FastAPI.
"""


class ErroDeDominio(Exception):
    """Base de todos os erros de regra de negócio."""

    codigo = "erro_de_dominio"

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class GrupoNaoEncontradoError(ErroDeDominio):
    codigo = "grupo_nao_encontrado"

    def __init__(self):
        super().__init__("Grupo não encontrado")


class MateriaNaoEncontradaError(ErroDeDominio):
    codigo = "materia_nao_encontrada"

    def __init__(self):
        super().__init__("Matéria não encontrada")


class MateriaInexistenteError(ErroDeDominio):
    codigo = "materia_inexistente"

    def __init__(self, materia_id: int):
        super().__init__(f"A matéria {materia_id} não existe")


class GrupoDuplicadoError(ErroDeDominio):
    codigo = "grupo_duplicado"

    def __init__(self):
        super().__init__("Já existe um grupo com esse nome nessa matéria")
