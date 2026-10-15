# Module 10, CRUD: Reading Data

[Português](../docs/10-crud-lendo-dados.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

With the models ready, you start building the real API. CRUD has four letters, and the **R** for *Read* is the simplest and most used, so that is where you start. In this module you implement the routes that list and fetch, including the **"not found"** response.

## // The problem: where the data comes from, and what to do when it does not exist

A read route needs two things: a place where the data is, and a decision about what to respond when the request points to something that does not exist. This week the data lives in memory, in Python dictionaries, and the "does not exist" decision is a `404`.

## // The project's data

Create the file `dados.py` ("data") in the `api-grupos` folder. It holds the sample subjects and groups (here, the start of the file; the full content is in `example/api-basica/dados.py`):

```python
import itertools
from datetime import datetime, timezone

MATERIAS = {
    1: {"materia_id": 1, "nome": "Cálculo I", "codigo": "MAT101"},
    2: {"materia_id": 2, "nome": "Estrutura de Dados", "codigo": "INF201"},
    # ... four more subjects
}


def _data(dia: int) -> datetime:
    return datetime(2026, 9, dia, 12, 0, tzinfo=timezone.utc)


GRUPOS = {
    1: {"grupo_id": 1, "nome_grupo": "Cálculo passo a passo", "materia_id": 1,
        "max_participantes": 6, "descricao": None, "criado_em": _data(1)},
    # ... five more groups
}

CONTADOR_GRUPOS = itertools.count(7)
```

The format is the one from Module 06: a dictionary of dictionaries, with the identifier as the key. `CONTADOR_GRUPOS` will generate the identifiers of the groups that get created (7, 8, 9, ...).

## // Preparing main.py

The final `main.py` starts like this:

```python
from fastapi import FastAPI, HTTPException, Response, status

import dados
from schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate, MateriaOut

app = FastAPI(title="API Central: Buscador de Grupos de Estudo", version="1.0.0")
```

Two new things: `import dados`, which brings in the data file as a module (so `dados.GRUPOS` is the groups dictionary), and `status`, a collection of readable names for the codes (`status.HTTP_404_NOT_FOUND` is 404).

## // Listing a collection

```python
@app.get("/materias", response_model=list[MateriaOut])
def listar_materias():
    return list(dados.MATERIAS.values())
```

`dados.MATERIAS.values()` returns each subject's dictionary, and `list(...)` turns them into a list. `response_model=list[MateriaOut]` says the response is a **list** of subjects, each one in the model's format.

```
GET /materias

200  [{"materia_id":1,"nome":"Cálculo I","codigo":"MAT101"}, ...]   (6 items)
```

## // Fetching one item and the 404

```python
@app.get("/materias/{materia_id}", response_model=MateriaOut)
def buscar_materia(materia_id: int):
    materia = dados.MATERIAS.get(materia_id)
    if materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria não encontrada")
    return materia
```

The reasoning is the one from Module 06: `.get()` returns `None` if the key does not exist, and the function decides what to do. The new ingredient is `HTTPException`:

> **HTTPEXCEPTION: IN SIMPLE WORDS**
> It is a special FastAPI exception. When you **raise** it with `raise`, the function stops there, and FastAPI turns the exception into an HTTP response with the code and message you chose.

```
GET /materias/1
200  {"materia_id":1,"nome":"Cálculo I","codigo":"MAT101"}

GET /materias/99
404  {"detail":"Matéria não encontrada"}
```

`raise` stops the function, which is why an `else` is **not needed**: `return materia` is only reached when the subject exists.

## // Reusing the 404: the helper function

Fetching a group will be used in four routes (fetch, replace, change and delete). Instead of repeating the `if` four times, it becomes a function:

```python
def buscar_grupo_ou_404(grupo_id: int) -> dict:
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
    return grupo


@app.get("/grupos/{grupo_id}", response_model=GrupoOut)
def buscar_grupo(grupo_id: int):
    return buscar_grupo_ou_404(grupo_id)
```

```
GET /grupos/3
200  {"nome_grupo":"Modelagem e SQL","materia_id":3,"max_participantes":8,"descricao":"Encontros online às terças e aos sábados","grupo_id":3,"criado_em":"2026-09-03T12:00:00Z"}

GET /grupos/99
404  {"detail":"Grupo não encontrado"}
```

The `HTTPException` raised **inside** the helper function also stops the route that called it. That is why the `buscar_grupo` route is a single line.

## // Listing with filters

The route that lists the groups accepts two optional query parameters, the search term `q` and the subject `materia_id`:

```python
@app.get("/grupos", response_model=list[GrupoOut])
def listar_grupos(q: str | None = None, materia_id: int | None = None):
    grupos = list(dados.GRUPOS.values())
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g["nome_grupo"].lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g["materia_id"] == materia_id]
    return grupos
```

The logic is the one from Module 06: you start with all the groups, and each filter **narrows** the list with a list comprehension. Calling `.lower()` on both sides makes the search ignore upper and lowercase.

```
GET /grupos?q=prática
200  [{"nome_grupo":"Estruturas na prática","materia_id":2, ... }]

GET /grupos?materia_id=1
200  [{"nome_grupo":"Cálculo passo a passo","materia_id":1, ... }]

GET /grupos?q=zzz
200  []
```

> **A SEARCH WITH NO RESULTS IS NOT A 404**
> Notice the last example: `GET /grupos?q=zzz` returns **200** with an **empty** list. The `404` is for when the **address** points to something that does not exist (`/grupos/99`). A collection that exists but has no item matching the filter is a valid response: the list is just empty.

## // Testing in Swagger

Open `/docs`. The `q` and `materia_id` parameters show up as optional text fields on the `GET /grupos` route, and the `grupo_id` field shows up as required on `GET /grupos/{grupo_id}`. Test:

1. `GET /grupos` without filling anything in.
2. `GET /grupos` with `q` equal to `prática`.
3. `GET /grupos/3`, and then `GET /grupos/99`.
4. `GET /grupos/abc` and read the `422`.

## // Good example × bad example

**Bad example**: returning `200` with a message when the item does not exist:

```python
@app.get("/grupos/{grupo_id}")
def buscar_grupo(grupo_id: int):
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        return {"mensagem": "grupo não encontrado"}
    return grupo
```

The client gets `200 OK` and has to open the body to find out it actually failed.

**Good example**: the code tells the truth:

```python
if grupo is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
```

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| A `KeyError` and a `500` when fetching a nonexistent id | Used `dados.GRUPOS[grupo_id]` instead of `.get()` | Use `.get()` and handle the `None` with `HTTPException` |
| `return HTTPException(...)` does not return a 404 | The `raise` is missing: the object was just returned as data | Use `raise HTTPException(...)` |
| The search returns `404` when nothing matches | Confusing "empty collection" with "nonexistent resource" | Return `200` with `[]` |
| The route returns a dictionary without the model's fields | The `response_model` expects fields the dictionary does not have | Check that the data has all of the model's fields |
| A change to the results list changes the original data | Changing a dictionary that came from `dados.GRUPOS` | Read without modifying in read routes |
| Error messages in English mixed with Portuguese | Default messages (`Not Found`) live alongside yours | Set each `HTTPException`'s `detail` in the project's language |

## // Guided practice

1. Create `dados.py` and `schemas.py` in the `api-grupos` folder (use the files from `example/api-basica` as a reference).
2. In `main.py`, write the `GET /materias` and `GET /materias/{materia_id}` routes.
3. Write the `buscar_grupo_ou_404` function and the `GET /grupos` and `GET /grupos/{grupo_id}` routes.
4. Test each one in Swagger, including an identifier that does not exist and a filter with no results.

## // Practice on your own

> **CHALLENGE**
> Add a third filter to the `GET /grupos` route, `min_vagas`, that keeps only the groups with `max_participantes` greater than or equal to the given value. Test `min_vagas=6` and `min_vagas=100`, and confirm the second one returns `200` with an empty list, not an error.

## // Applying it to the week's project

1. Get the read routes working in the `main.py` of the `api-grupos` folder.
2. Go through the five test cases from the previous section in Swagger and write down, in the `README.md`, the code each one returned.
3. If you version the project with Git, make a commit: `git commit -m "Implement the read routes"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> What is the difference between `GET /grupos/99` and `GET /grupos?materia_id=99`, in terms of the returned status code?

Answer: `GET /grupos/99` points to **a specific item** that does not exist, so it returns `404`. `GET /grupos?materia_id=99`, on the other hand, asks for the **collection** of groups filtered by a subject. The collection exists, and the filter just finds no items, so the response is `200` with `[]`. The address says who you are looking for, and the filter says which items of the collection you want to see.

## // Module summary

- [ ] I can store data in dictionaries and import the `dados` module.
- [ ] I can write a route that lists a collection, with `response_model=list[...]`.
- [ ] I can fetch an item and respond `404` with `HTTPException`.
- [ ] I can reuse the `404` in a helper function.
- [ ] I can implement optional filters with query parameters.
- [ ] I know a search with no results returns `200` with an empty list.

---

**Next module:** `11-crud-creating-updating-and-deleting.md`: reading is ready. The rest of CRUD is missing: creating, updating and deleting.

`Study Material // Coffee & Code`
