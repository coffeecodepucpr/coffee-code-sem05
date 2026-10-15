# Module 14, Organizing an API in Layers

[Português](../docs/14-organizando-uma-api-em-camadas.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

> **EXPERIENCED TRACK**
> This module is part of the experienced track: it comes after the essential content and is not needed for the week's deliverable. Anyone following the main track can skip to `deliverable.md`.

The main track's API fits in a single `main.py`, and that is great for learning. But a file with all the routes, all the rules and all the data stops being workable when the API grows. This module splits the API into **packages and layers**, without changing any of its responses, and ends by showing a problem that splitting alone does not solve. Module 15 solves that problem.

## // The problem: a file that does everything

A 300-line `main.py` mixes creating the application, the group routes, the subject routes and the business rules. Finding where to change a rule means scrolling through the whole file, and a change in one route risks breaking another. The solution is to give each responsibility its own file.

## // Package and APIRouter

> **PACKAGE: IN SIMPLE WORDS**
> It is a folder of Python files that can be imported as a set. The `__init__.py` file (which can be empty) is what tells Python the folder is a package.

> **APIROUTER: IN SIMPLE WORDS**
> It is an object that groups a resource's routes, like a "mini-application". It is created in its own file, and then connected to the main application.

The structure of the package version (`example/api-em-pacotes/`):

```
api-em-pacotes/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dados.py
│   ├── schemas.py
│   ├── regras.py
│   └── routers/
│       ├── __init__.py
│       ├── grupos.py
│       └── materias.py
└── requirements.txt
```

| File | Responsibility |
|---|---|
| `main.py` | Creates the application and connects the routers. It has almost no logic |
| `routers/grupos.py` and `routers/materias.py` | Only each resource's routes |
| `regras.py` | The reused business rules (404, 422 and 409) |
| `schemas.py` | The Pydantic models |
| `dados.py` | The in-memory data |

<div align="center">
<img src="../docs/assets/estrutura-projeto-fastapi.svg" alt="Who imports whom in the package project: main, routers, regras, schemas and dados" width="640">
</div>

The start of `routers/grupos.py`:

```python
from fastapi import APIRouter, Response, status

from app import dados, regras
from app.schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate

router = APIRouter(prefix="/grupos", tags=["grupos"])


@router.get("", response_model=list[GrupoOut], summary="Lista os grupos")
def listar_grupos(q: str | None = None, materia_id: int | None = None):
    ...
```

Two changes compared to the main track's `main.py`:

- The decorator is no longer `@app.get(...)` but `@router.get(...)`.
- `prefix="/grupos"` and `tags=["grupos"]` are defined **once**, in the router. That is why the list route uses the path `""` (empty): the final address is the prefix plus the path. The route that fetches one item uses `"/{grupo_id}"`, and the final address is `/grupos/{grupo_id}`.

And `main.py` gets small, it only connects the pieces:

```python
from fastapi import FastAPI

from app.routers import grupos, materias

app = FastAPI(title="API Central: Buscador de Grupos de Estudo", description=DESCRICAO, version="1.1.0", openapi_tags=[...])

app.include_router(materias.router)
app.include_router(grupos.router)
```

## // Absolute imports

Inside a package, imports start with the package name:

```python
from app import dados, regras
from app.schemas import GrupoCreate
```

That is why the folder is called `app`: it is the starting point for every import.

## // Running the package project

The command only changes the file path. In the `api-em-pacotes` folder:

```
fastapi dev app/main.py
```

```
Using import string: app.main:app

Server started at http://127.0.0.1:8000
Documentation at http://127.0.0.1:8000/docs
```

Notice `app.main:app`: it is the package path (`app.main`) and the object's name (`app`). FastAPI's documentation also describes a way to register this path in the project's configuration file (`[tool.fastapi]` with `entrypoint`), so that typing `fastapi dev` is enough; that option was not tested here.

## // The three layers

<div align="center">
<img src="../docs/assets/camadas-da-api.svg" alt="The three layers of the package project: routes, rules and data, and the problem that still bothers the rules layer" width="640">
</div>

The split creates, in practice, **layers**, and each one has a role:

| Layer | File | What it decides |
|---|---|---|
| **Routes** | `routers/*.py` | How the HTTP request comes in and how the response goes out |
| **Rules** | `regras.py` | What the system allows: does the subject exist? is the name free? does the group exist? |
| **Data** | `dados.py` | Where the information is stored |

A golden rule of layers: **each one should only talk to the one right below it**. The route calls the rule, and the rule reads the data. Never the other way around.

### > What does not change

Splitting is a change in **organization**, not in behavior. The proof, in this version: `/openapi.json` lists the same four paths (`/materias`, `/materias/{materia_id}`, `/grupos` and `/grupos/{grupo_id}`) with the same methods, and the requests from Module 13's test script return the same codes.

## // What still bothers us

Open `regras.py`:

```python
from fastapi import HTTPException, status

from app import dados


def buscar_grupo_ou_404(grupo_id: int) -> dict:
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
    return grupo
```

Notice the first line: `from fastapi import HTTPException`. The **rules** layer, which should only know about the group system, imported the web framework. Three consequences:

- **Testing a rule requires FastAPI.** To check that "nonexistent group" is an error, you have to deal with `HTTPException` and status codes, which are an HTTP matter, not the rule's.
- **The rule knows the status code.** Whoever decides that "not found" is `404` should be the routes layer, the only one that speaks HTTP.
- **Switching frameworks forces you to rewrite the rules.** If one day the same rule needs to serve another kind of program (a terminal script, for example), it comes "contaminated" by HTTP.

Splitting into files organized the code, but **did not invert the dependency**: the rules still depend on the framework. Module 15 shows how to turn this around.

## // Good example × bad example

**Bad example**: copying the rules into each router:

```python
# in routers/grupos.py
def conferir_materia(materia_id): ...

# in routers/outro.py
def conferir_materia(materia_id): ...   # a copy that will one day drift apart
```

Two copies of the same rule end up different: someone fixes one and forgets the other.

**Good example**: a single definition in `regras.py`, imported by whoever needs it:

```python
from app import regras

regras.conferir_materia(novo.materia_id)
```

## // Common mistakes

These messages were obtained by running the code.

| Mistake | What it says | Why it happens | How to fix it |
|---|---|---|---|
| `ModuleNotFoundError` | `No module named 'dados'` | An import inside the package was left as `import dados` | Use `from app import dados` |
| `ModuleNotFoundError` | `No module named 'app'` | The command was run outside the folder that contains `app` | Go into the project folder before running |
| An import fails in a strange way | (varies) | The `__init__.py` is missing in one of the folders | Create the empty file in `app` and in `app/routers` |
| A router's routes do not show up in `/docs` | (no message) | The `app.include_router(...)` is missing | Connect each router in `main.py` |
| The final address became `/grupos/grupos` | (no message) | The prefix was repeated in the decorator and in the router | Define the prefix only in the `APIRouter` |

## // Guided practice

1. Create the `api-em-pacotes` folder, with `app` and `app/routers`, and the two empty `__init__.py` files.
2. Move the models to `app/schemas.py`, the data to `app/dados.py` and the three rule functions to `app/regras.py`.
3. Create `app/routers/materias.py` and `app/routers/grupos.py` with `APIRouter` and move the routes from `main.py` into them.
4. Rewrite `app/main.py` with only the application's creation and the two `include_router` calls.
5. Run `fastapi dev app/main.py`, open `/docs` and check that all the routes are still there.

## // Practice on your own

> **CHALLENGE**
> Create a third router, `routers/saude.py` ("health"), with a single `GET /saude` route that returns `{"status": "ok"}`. Use the `APIRouter`'s prefix and tags, connect it in `main.py` and confirm it shows up in `/docs` in its own group. Then look through your code for **all** the files that import something from `fastapi` and note which of them are not routes: that is the list of what Module 15 will clean up.

## // Applying it to the week's project

1. If you followed the experienced track, keep the package version in a separate folder, without deleting the main track's `api-grupos`.
2. Check that the `/openapi.json` of both versions lists the same paths.
3. If you version the project with Git, make a commit: `git commit -m "Split the API into packages and routers"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You moved the group routes to a router with `prefix="/grupos"`, but kept the path `"/grupos"` in the list decorator. What will the route's address be, and how do you fix it?

Answer: the final address will be `/grupos/grupos`, because the router's prefix is added to the decorator's path. The fix is to use the empty path (`@router.get("")`) for the list route, and `"/{grupo_id}"` for the single-item ones, leaving `/grupos` only in the `prefix`.

## // Module summary

- [ ] I can split the API into a package, with `__init__.py` and absolute imports.
- [ ] I can create an `APIRouter` with a prefix and tags, and connect it with `include_router`.
- [ ] I can describe the three layers (routes, rules and data) and each one's role.
- [ ] I can run a package project with `fastapi dev app/main.py`.
- [ ] I can explain why `from fastapi import HTTPException` inside the rules is a problem.

---

**Next module:** `15-clean-architecture-in-fastapi.md`: the layers exist, but the dependency still points the wrong way. Time to invert it.

`Study Material // Coffee & Code`
