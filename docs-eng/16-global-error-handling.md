# Module 16, Global Error Handling

[Português](../docs/16-tratamento-global-de-erros.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

> **EXPERIENCED TRACK**
> This module is part of the experienced track: it comes after the essential content and is not needed for the week's deliverable. Anyone following the main track can skip to `deliverable.md`.

In Module 15 the rules started raising errors that do not know HTTP, like `GrupoNaoEncontradoError`. The piece that closes the loop is missing: **whoever turns each error into a response**. This module introduces FastAPI's *exception handlers*, which do this in **a single place**, and defines one error format for the whole API. The complete code is in `example/api-limpa/app/api/erros.py`.

## // The problem: every error looks different

In the main track's API, the client receives errors in different formats, depending on where they come from. These are real responses:

| Situation | Response body | Format |
|---|---|---|
| Nonexistent group (`404`) | `{"detail":"Grupo não encontrado"}` | `detail` is a **string** |
| Invalid data (`422`) | `{"detail":[{...}]}` | `detail` is a **list** of objects |
| A route that does not exist (`404`) | `{"detail":"Not Found"}` | `detail` in English |
| Method not allowed (`405`) | `{"detail":"Method Not Allowed"}` | `detail` in English |
| Programming error (`500`) | `Internal Server Error` | **Plain text**, not even JSON |

Whoever writes a client (a screen, another program) has to handle five different formats just to read an error message. And, in a growing API, each route tends to invent yet another way.

## // What an exception handler is

> **EXCEPTION HANDLER: IN SIMPLE WORDS**
> It is a function you register for an **exception type**. Whenever an exception of that type goes up to the end of a route without being handled, FastAPI calls that function, and whatever it returns becomes the response.

<div align="center">
<img src="../docs/assets/fluxo-de-erros.svg" alt="The path of a domain error until it becomes an HTTP response, and the four registered handlers" width="640">
</div>

The advantage is twofold: the **rules** do not need to know about HTTP (they just raise the error), and the **routes** do not need `try/except` (the error goes up on its own to the handler).

## // A single error format

First, you decide **what every error will look like**. In this API, it is always an object with three fields:

```json
{
  "erro": "grupo_nao_encontrado",
  "mensagem": "Grupo não encontrado",
  "detalhes": null
}
```

| Field | What it is |
|---|---|
| `erro` ("error") | A short, stable code, made for **programs** to read (it does not change if the message is translated) |
| `mensagem` ("message") | The text for **people** to read |
| `detalhes` ("details") | A list with the specific points of the problem (used in validation), or `null` |

The code builds this response in a single function:

```python
def resposta_de_erro(status_code: int, erro: str, mensagem: str, detalhes=None, headers=None) -> JSONResponse:
    corpo = {"erro": erro, "mensagem": mensagem, "detalhes": detalhes}
    return JSONResponse(status_code=status_code, content=corpo, headers=headers)
```

## // Handler 1: domain errors

Here comes the missing map: which **status code** each domain error becomes. It exists in **one** place, and only in the API layer:

```python
STATUS_POR_ERRO = {
    GrupoNaoEncontradoError: 404,
    MateriaNaoEncontradaError: 404,
    MateriaInexistenteError: 422,
    GrupoDuplicadoError: 409,
}


def registrar_tratadores(app: FastAPI) -> None:
    @app.exception_handler(ErroDeDominio)
    async def tratar_erro_de_dominio(request: Request, erro: ErroDeDominio):
        return resposta_de_erro(STATUS_POR_ERRO.get(type(erro), 400), erro.codigo, erro.mensagem)
```

The handler is registered for `ErroDeDominio`, the **base class**. That is why it also catches all its children (`GrupoNaoEncontradoError` and the others). Real responses:

```
GET /grupos/99

404  {"erro":"grupo_nao_encontrado","mensagem":"Grupo não encontrado","detalhes":null}

POST /grupos   {"nome_grupo":"Grupo fantasma","materia_id":99}

422  {"erro":"materia_inexistente","mensagem":"A matéria 99 não existe","detalhes":null}
```

Notice the routes did not change at all: `buscar_grupo` is still `return servico.buscar(grupo_id)`. The error goes up on its own.

## // Handler 2: FastAPI's validation errors

The automatic `422`s (invalid data) can also be translated into the single format, with the `RequestValidationError` type:

```python
@app.exception_handler(RequestValidationError)
async def tratar_validacao(request: Request, erro: RequestValidationError):
    detalhes = [{"campo": ".".join(str(parte) for parte in e["loc"]), "mensagem": e["msg"]} for e in erro.errors()]
    return resposta_de_erro(422, "validacao", "Os dados enviados são inválidos", detalhes)
```

The `loc` you know (`["body", "nome_grupo"]`) becomes the text `body.nome_grupo`. Two real responses ("The data sent is invalid"):

```
POST /grupos   {"nome_grupo":"ab","materia_id":0}

422  {"erro":"validacao","mensagem":"Os dados enviados são inválidos","detalhes":[
       {"campo":"body.nome_grupo","mensagem":"String should have at least 3 characters"},
       {"campo":"body.materia_id","mensagem":"Input should be greater than 0"}]}

GET /grupos/abc

422  {"erro":"validacao","mensagem":"Os dados enviados são inválidos","detalhes":[
       {"campo":"path.grupo_id","mensagem":"Input should be a valid integer, unable to parse string as an integer"}]}
```

(The `detalhes` were split across several lines here to fit the page; the real response comes on a single line.) Module 09's `PATCH` with `null` goes through the same path, and the response points to `body.nome_grupo`.

## // Handler 3: the framework's own HTTP errors

When the route does not even exist, or the method is not accepted, the error is raised by the framework, with Starlette's `HTTPException` class (the base FastAPI is built on):

```python
CODIGO_POR_STATUS = {404: "nao_encontrado", 405: "metodo_nao_permitido"}
MENSAGEM_POR_STATUS = {404: "Recurso não encontrado", 405: "Método não permitido para este recurso"}


@app.exception_handler(StarletteHTTPException)
async def tratar_erro_http(request: Request, erro: StarletteHTTPException):
    codigo = CODIGO_POR_STATUS.get(erro.status_code, "erro_http")
    mensagem = MENSAGEM_POR_STATUS.get(erro.status_code, str(erro.detail))
    return resposta_de_erro(erro.status_code, codigo, mensagem, headers=getattr(erro, "headers", None))
```

An important note: the handler is registered for **Starlette's** class, not FastAPI's. FastAPI's `HTTPException` is a child of Starlette's, so registering the parent class catches both.

```
GET /nada

404  {"erro":"nao_encontrado","mensagem":"Recurso não encontrado","detalhes":null}

DELETE /grupos

405  {"erro":"metodo_nao_permitido","mensagem":"Método não permitido para este recurso","detalhes":null}
     allow: GET
```

The `headers=` parameter exists so the `405`'s `allow` header is **not lost**, since it tells the client which methods the route accepts. A handler that forgets the original exception's headers erases useful information.

## // Handler 4: the unexpected error

The last handler is the safety net: any error **nobody foresaw** (a bug, a division by zero):

```python
@app.exception_handler(Exception)
async def tratar_erro_inesperado(request: Request, erro: Exception):
    logger.exception("Erro inesperado em %s %s", request.method, request.url.path)
    return resposta_de_erro(500, "erro_interno", "Erro interno do servidor")
```

Two security decisions are in this code:

- **The client does not get the detail.** The response is always the same generic message. Internal details (file names, code snippets, values) help whoever wants to attack the system.
- **The detail goes to the log.** `logger.exception` records the full error, with the call chain, for whoever maintains the API to investigate.

Tested on a real server, with a route that raises `RuntimeError("detalhe interno secreto")` ("secret internal detail"):

```
(what the client receives)
HTTP/1.1 500 Internal Server Error
{"erro":"erro_interno","mensagem":"Erro interno do servidor","detalhes":null}

(what the server log records)
Erro inesperado em GET /quebra
    def quebra(): raise RuntimeError("detalhe interno secreto")
RuntimeError: detalhe interno secreto
INFO:     127.0.0.1:43836 - "GET /quebra HTTP/1.1" 500 Internal Server Error
```

The client never saw the word "secreto". The log kept everything.

> **A DETAIL ABOUT TESTS**
> In a test, `TestClient` **raises the unexpected error again**, even with the handler responding `500`. That is on purpose (so tests do not hide bugs). To test the `500` in JSON, create the client like this: `TestClient(app, raise_server_exceptions=False)`.

## // The right handler for each error

FastAPI picks the handler by the error's **type**, from the most specific to the most general. That is why the registration order does not matter, and a domain error **never** falls into the generic `Exception` handler:

| Error type | Handler | Response |
|---|---|---|
| `GrupoNaoEncontradoError` (and its siblings) | `ErroDeDominio` | `404`, `409` or `422` |
| Data that Pydantic rejected | `RequestValidationError` | `422` with the list of fields |
| A nonexistent route or method | `StarletteHTTPException` | `404` or `405` |
| Anything else | `Exception` | A generic `500`, and the detail goes to the log |

## // Documenting the format in Swagger

A problem shows up: FastAPI keeps describing the `422` with the **old format** in the documentation, even though the API returns the new one. The real `/openapi.json` response, before the fix, for `GET /grupos/{grupo_id}`:

```
200 -> GrupoOut     404 -> ErroOut     422 -> HTTPValidationError
```

The `422` still pointed to FastAPI's default model. The fix is to declare the error model in the **router's** `responses`, which applies to all of its routes:

```python
router = APIRouter(
    prefix="/grupos",
    tags=["grupos"],
    responses={422: {"model": ErroOut, "description": "Dados inválidos (formato único de erro)"}},
)
```

After the fix:

```
200 -> GrupoOut     422 -> ErroOut     404 -> ErroOut
```

Now Swagger and the API tell the same story. Remember: the documentation is a promise, and a client that reads it needs to be able to trust it.

## // Registering the handlers

In `main.py`, one line wires everything up:

```python
app = FastAPI(title="API Central: Buscador de Grupos de Estudo", ...)

registrar_tratadores(app)
app.include_router(materias.router)
app.include_router(grupos.router)
```

The `registrar_tratadores` function receives the `app` and registers all four. This keeps `main.py` small and leaves all error handling in **a single file**, easy to read and to test.

## // Good example × bad example

**Bad example**: a `try/except` in every route:

```python
@router.get("/{grupo_id}")
def buscar_grupo(grupo_id: int, servico: ServicoGruposDep):
    try:
        return servico.buscar(grupo_id)
    except GrupoNaoEncontradoError:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
```

Translating the error becomes **repeated code** in every route, the error format depends on who wrote each one, and forgetting the `except` in one route turns into a `500`.

**Good example**: the route handles nothing, and the global handler translates:

```python
@router.get("/{grupo_id}")
def buscar_grupo(grupo_id: int, servico: ServicoGruposDep):
    return servico.buscar(grupo_id)
```

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| The handler is never called | It was registered for the wrong class, or `registrar_tratadores(app)` was not called | Check the error type and the line in `main.py` |
| The `405` lost the `allow` header | The handler did not pass on the exception's headers | Use `headers=getattr(erro, "headers", None)` |
| The client receives internal details in the `500` | The handler returns `str(erro)` | Return a fixed message and record the detail in the log |
| Swagger shows the old error format | `responses` does not declare the new model | Declare `responses={422: {"model": ErroOut}}` in the router |
| The `500` test raises the exception | `TestClient` re-raises unexpected errors | Use `raise_server_exceptions=False` |
| A new domain error becomes a `400` | It is not in `STATUS_POR_ERRO` | Add the type to the map |

## // Guided practice

1. Read the whole `app/api/erros.py` and connect each function to the handler in the table.
2. Run the API (`fastapi dev app/main.py`) and trigger each response in the module: `GET /grupos/99`, `GET /grupos/abc`, `GET /nada`, `DELETE /grupos`. Check the single format in all of them.
3. Compare each response with the main track API's (the table at the start of the module).
4. Temporarily add a route that raises any error, call it, and compare what the client received with what the terminal recorded.

## // Practice on your own

> **CHALLENGE**
> Add a new rule to the domain: reserved names, like `admin`, cannot be used as a group name. Create the `NomeReservadoError` error in `dominio/erros.py`, raise it in the service's `criar`, and register it in `STATUS_POR_ERRO` with status `422`. Check that you touched **three** places (domain, application and API) and that **no route** had to change. Write a test that confirms the `422` and the `nome_reservado` code.

## // Applying it to the week's project

1. If you followed the experienced track, create `app/api/erros.py` in your layered API and register the four handlers in `main.py`.
2. Declare `ErroOut` in your routers' `responses`.
3. If you version the project with Git, make a commit: `git commit -m "Add global error handling"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> The domain error `GrupoNaoEncontradoError` is a child of `ErroDeDominio`, which in turn is a child of `Exception`. There are handlers registered for both. Which one responds, and why?

Answer: the `ErroDeDominio` one. FastAPI looks for the handler of the **most specific** type that fits the error, and `ErroDeDominio` is more specific than `Exception`. The `Exception` one only responds to errors no other handler recognizes. That is why a nonexistent group becomes a `404` in the single format, and only a real bug becomes a `500`.

## // Module summary

- [ ] I know what an exception handler is and when FastAPI calls it.
- [ ] I can define a single error format (`erro`, `mensagem` and `detalhes`).
- [ ] I can map domain errors to status codes in a single place.
- [ ] I can translate validation errors and the framework's own HTTP errors.
- [ ] I know why the `500` does not return details to the client, and where they are recorded.
- [ ] I can document the error format in Swagger with `responses`.

---

**Next module:** `17-automated-tests.md`, a bonus module in the experienced track, or `deliverable.md` for the final review.

`Study Material // Coffee & Code`
