"""Tratamento global de erros: a ÚNICA tradução de erros para respostas HTTP.

Os erros do domínio não sabem o que é HTTP. Este arquivo decide, em um só
lugar, qual código de status e qual corpo cada erro vira.
"""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.dominio.erros import (
    ErroDeDominio,
    GrupoDuplicadoError,
    GrupoNaoEncontradoError,
    MateriaInexistenteError,
    MateriaNaoEncontradaError,
)

logger = logging.getLogger("api")

STATUS_POR_ERRO = {
    GrupoNaoEncontradoError: 404,
    MateriaNaoEncontradaError: 404,
    MateriaInexistenteError: 422,
    GrupoDuplicadoError: 409,
}

CODIGO_POR_STATUS = {404: "nao_encontrado", 405: "metodo_nao_permitido"}
MENSAGEM_POR_STATUS = {404: "Recurso não encontrado", 405: "Método não permitido para este recurso"}


def resposta_de_erro(status_code: int, erro: str, mensagem: str, detalhes=None, headers=None) -> JSONResponse:
    corpo = {"erro": erro, "mensagem": mensagem, "detalhes": detalhes}
    return JSONResponse(status_code=status_code, content=corpo, headers=headers)


def registrar_tratadores(app: FastAPI) -> None:
    @app.exception_handler(ErroDeDominio)
    async def tratar_erro_de_dominio(request: Request, erro: ErroDeDominio):
        return resposta_de_erro(STATUS_POR_ERRO.get(type(erro), 400), erro.codigo, erro.mensagem)

    @app.exception_handler(RequestValidationError)
    async def tratar_validacao(request: Request, erro: RequestValidationError):
        detalhes = [{"campo": ".".join(str(parte) for parte in e["loc"]), "mensagem": e["msg"]} for e in erro.errors()]
        return resposta_de_erro(422, "validacao", "Os dados enviados são inválidos", detalhes)

    @app.exception_handler(StarletteHTTPException)
    async def tratar_erro_http(request: Request, erro: StarletteHTTPException):
        codigo = CODIGO_POR_STATUS.get(erro.status_code, "erro_http")
        mensagem = MENSAGEM_POR_STATUS.get(erro.status_code, str(erro.detail))
        return resposta_de_erro(erro.status_code, codigo, mensagem, headers=getattr(erro, "headers", None))

    @app.exception_handler(Exception)
    async def tratar_erro_inesperado(request: Request, erro: Exception):
        logger.exception("Erro inesperado em %s %s", request.method, request.url.path)
        return resposta_de_erro(500, "erro_interno", "Erro interno do servidor")
