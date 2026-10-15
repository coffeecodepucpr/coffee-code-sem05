# Module 11, CRUD: Creating, Updating and Deleting

[Português](../docs/11-crud-criar-atualizar-e-apagar.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

Reading does not change anything, which is why it is the simplest part of CRUD. This module covers the three letters that **change** the data: **C**reate, **U**pdate and **D**elete. This is where the `201`, `204` and `409` codes show up, and where the choice of method and code matters most.

## // The problem: changing data requires care

Reading is harmless. Creating, replacing and deleting are not: a mistake creates a duplicate group, deletes the wrong group or leaves broken data. That is why each of these operations needs to **check** what arrived before touching anything, and **respond precisely** with what happened.

## // The project's rules

Before the code, it is worth deciding the rules. The project's API follows these:

| Rule | If it is broken |
|---|---|
| The `materia_id` must exist | `422` |
| The fields must respect the model (name of 3 to 60 characters, limit of 2 to 50) | `422` |
| There cannot be two groups with the same name **in the same subject** (case-insensitive) | `409` |
| The group to change or delete must exist | `404` |

These two helper functions check the two rules that live outside the model:

```python
def conferir_materia(materia_id: int) -> None:
    if materia_id not in dados.MATERIAS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"A matéria {materia_id} não existe",
        )


def conferir_nome_livre(nome_grupo: str, materia_id: int, ignorar_id: int | None = None) -> None:
    for grupo in dados.GRUPOS.values():
        mesmo_nome = grupo["nome_grupo"].lower() == nome_grupo.lower()
        if mesmo_nome and grupo["materia_id"] == materia_id and grupo["grupo_id"] != ignorar_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um grupo com esse nome nessa matéria",
            )
```

The `ignorar_id` ("ignore id") parameter exists for the update routes: a group can keep its own name, it just cannot take **another** group's name.

## // Creating: POST and the 201

```python
@app.post("/grupos", response_model=GrupoOut, status_code=status.HTTP_201_CREATED)
def criar_grupo(novo: GrupoCreate, response: Response):
    conferir_materia(novo.materia_id)
    conferir_nome_livre(novo.nome_grupo, novo.materia_id)
    grupo_id = next(dados.CONTADOR_GRUPOS)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": datetime.now(timezone.utc)}
    dados.GRUPOS[grupo_id] = grupo
    response.headers["Location"] = f"/grupos/{grupo_id}"
    return grupo
```

Step by step:

1. `novo: GrupoCreate` reads and validates the JSON body (Module 09).
2. The two checks can raise `422` or `409`.
3. `next(dados.CONTADOR_GRUPOS)` generates the next identifier (Module 06).
4. `{**novo.model_dump(), ...}` builds the group's dictionary by joining the fields sent with the ones the API generates. The `**` "spreads" the contents of one dictionary into another.
5. The group is stored in `dados.GRUPOS`.
6. The `Location` header states the new group's address.
7. `status_code=201` in the decorator sets the route's **success** code.

```
POST /grupos   {"nome_grupo":"Cálculo II na prática","materia_id":1,"max_participantes":5}

201 Created
location: /grupos/7
{"nome_grupo":"Cálculo II na prática","materia_id":1,"max_participantes":5,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

And the errors, all obtained from the running API:

```
POST /grupos   (the same body, again)
409  {"detail":"Já existe um grupo com esse nome nessa matéria"}

POST /grupos   {"nome_grupo":"Grupo fantasma","materia_id":99}
422  {"detail":"A matéria 99 não existe"}

POST /grupos   {"nome_grupo":"ab","materia_id":1}
422  {"detail":[{"type":"string_too_short","loc":["body","nome_grupo"], ... }]}
```

Two notes about the rules: the same name **in another subject** is accepted (`201`), and the comparison ignores upper and lowercase (creating `CÁLCULO PASSO A PASSO` in subject 1 returns `409`, because `Cálculo passo a passo` already exists there).

## // Replacing: PUT

`PUT` swaps the **whole** group (Module 03):

```python
@app.put("/grupos/{grupo_id}", response_model=GrupoOut)
def substituir_grupo(grupo_id: int, novo: GrupoUpdate):
    antigo = buscar_grupo_ou_404(grupo_id)
    conferir_materia(novo.materia_id)
    conferir_nome_livre(novo.nome_grupo, novo.materia_id, ignorar_id=grupo_id)
    grupo = {**novo.model_dump(), "grupo_id": grupo_id, "criado_em": antigo["criado_em"]}
    dados.GRUPOS[grupo_id] = grupo
    return grupo
```

The identifier and the creation date **do not change**: they come from the old group. Everything else comes from the body.

```
PUT /grupos/7   {"nome_grupo":"Cálculo II revisado","materia_id":1,"max_participantes":6}

200  {"nome_grupo":"Cálculo II revisado","materia_id":1,"max_participantes":6,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

If the `PUT` omits an optional field, it **goes back to the default value**. Sending only `nome_grupo` and `materia_id` makes `max_participantes` go back to 10 and `descricao` become `null`.

## // Changing part: PATCH

`PATCH` changes only what was sent:

```python
@app.patch("/grupos/{grupo_id}", response_model=GrupoOut)
def alterar_grupo(grupo_id: int, mudancas: GrupoPatch):
    grupo = buscar_grupo_ou_404(grupo_id)
    campos = mudancas.model_dump(exclude_unset=True)
    if "materia_id" in campos:
        conferir_materia(campos["materia_id"])
    nome = campos.get("nome_grupo", grupo["nome_grupo"])
    materia = campos.get("materia_id", grupo["materia_id"])
    conferir_nome_livre(nome, materia, ignorar_id=grupo_id)
    grupo.update(campos)
    return grupo
```

`exclude_unset=True` (Module 09) guarantees that only the fields sent go into `campos`. `grupo.update(campos)` overwrites only those keys in the dictionary. The `nome` and `materia` lines calculate the **final result** (what will remain after the change), to check that it does not collide with another group.

```
PATCH /grupos/7   {"max_participantes":8}

200  {"nome_grupo":"Cálculo II revisado","materia_id":1,"max_participantes":8,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

Only `max_participantes` changed, from 6 to 8.

> **VALIDATE BEFORE CHANGING**
> The order of the `PATCH` lines matters: first **all the checks** (subject exists, name is free), and only at the end `grupo.update(campos)`. If the change happened before a check failed, the group would be half changed. The same care applies to `null` values: Module 09's `GrupoPatch` model rejects `null` in `nome_grupo`, `materia_id` and `max_participantes` with a `422`, precisely so that an invalid value never reaches the part that saves. Without this protection, a single `PATCH` with `{"max_participantes": null}` corrupted the group and made the whole list return `500`.

## // Deleting: DELETE and the 204

```python
@app.delete("/grupos/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_grupo(grupo_id: int):
    buscar_grupo_ou_404(grupo_id)
    del dados.GRUPOS[grupo_id]
```

Notice that the function **returns nothing**: `204` means "it worked, and there is no content". Check the full response and the second attempt:

```
DELETE /grupos/7

HTTP/1.1 204 No Content
(no body)

DELETE /grupos/7   (again)

HTTP/1.1 404 Not Found
{"detail":"Grupo não encontrado"}
```

It is Module 03's idempotence in practice: the second call returns a different code, but the final state is the same (group 7 does not exist).

> **THE 204 CARRIES NO BODY**
> Code `204` means "no content", and the response body stays empty. In this week's tests, even a function that returned a dictionary in a route declared with `204` did not send any body: FastAPI discarded it. Even so, let the function end **without** a `return`: the code is more honest, and whoever reads it understands the route really returns nothing.

## // Which code to return: the CRUD map

<div align="center">
<img src="../docs/assets/qual-status-devolver.svg" alt="Decision tree leading from the CRUD operation to the correct status code" width="640">
</div>

| Operation | Success | Possible errors |
|---|---|---|
| `GET /grupos` | `200` | `422` (invalid parameter) |
| `GET /grupos/{id}` | `200` | `404`, `422` |
| `POST /grupos` | `201` | `409`, `422` |
| `PUT /grupos/{id}` | `200` | `404`, `409`, `422` |
| `PATCH /grupos/{id}` | `200` | `404`, `409`, `422` |
| `DELETE /grupos/{id}` | `204` | `404`, `422` |

## // A detail about curl and JSON

When testing with `curl` (Module 02), remember `-H "Content-Type: application/json"` on every `POST`, `PUT` and `PATCH`. Without it, any of the three returns the "Input should be a valid dictionary" `422`. Swagger sends the right header on its own.

## // Good example × bad example

**Bad example**: creating without checking anything:

```python
@app.post("/grupos")
def criar_grupo(novo: GrupoCreate):
    dados.GRUPOS[len(dados.GRUPOS) + 1] = novo.model_dump()
    return "ok"
```

This code uses the dictionary's size as the identifier (if a group is deleted, it **reuses** a number or overwrites another group), ignores the subject and duplicates, does not generate `criado_em`, and returns loose text with `200`.

**Good example**: checking, generating the identifier safely and responding well:

```python
@app.post("/grupos", response_model=GrupoOut, status_code=status.HTTP_201_CREATED)
def criar_grupo(novo: GrupoCreate, response: Response):
    conferir_materia(novo.materia_id)
    conferir_nome_livre(novo.nome_grupo, novo.materia_id)
    grupo_id = next(dados.CONTADOR_GRUPOS)
    ...
```

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| The route returns `200` when creating | `status_code=201` missing in the decorator | Add `status_code=status.HTTP_201_CREATED` |
| `DELETE` returns `200` with `null` | `status_code=204` missing in the decorator | Add `status_code=status.HTTP_204_NO_CONTENT` |
| `PATCH` erases fields that were not sent | `exclude_unset=True` is missing | Use `model_dump(exclude_unset=True)` |
| `PATCH` with `null` returns `500` and corrupts the data | The model accepts `null` in a field that cannot be empty | Validate with `field_validator` (Module 09) |
| `PUT` and `PATCH` return `409` when keeping their own name | The duplicate check does not ignore the group itself | Pass `ignorar_id=grupo_id` |
| Two groups get the same identifier | The identifier was calculated with `len(...)` | Use a counter (`next`) that never goes back |
| `422` when sending JSON with `curl` | The `Content-Type` is missing | Add `-H "Content-Type: application/json"` |
| The data disappeared | The server was restarted | That is expected: the data lives in memory |

## // Guided practice

1. Write the `conferir_materia` and `conferir_nome_livre` functions in `main.py`.
2. Write the `POST /grupos` route. In Swagger, create a group, then repeat it to get the `409`, then try a nonexistent `materia_id` and a name that is too short.
3. Write `PUT` and `PATCH`. Test a `PUT` with only the required fields and watch `max_participantes` go back to 10.
4. Write the `DELETE`. Delete a group twice in a row and compare the responses.
5. Check, in `GET /grupos`, that the list reflects each change.

## // Practice on your own

> **CHALLENGE**
> Add a rule to `POST /grupos` that the model does not cover: the group name **cannot be made only of digits** (like `"12345"`). Use the text method `isdigit()`, and return `422` with the message "The group name cannot be only digits". Test with `"12345"` and with `"Grupo 12345"` (the latter should be accepted).

## // Applying it to the week's project

1. Complete `main.py` with the `POST`, `PUT`, `PATCH` and `DELETE` routes.
2. In the `README.md`, fill in the CRUD map's code table with what you actually got when testing each operation.
3. If you version the project with Git, make a commit: `git commit -m "Implement creating, updating and deleting groups"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> A `PUT /grupos/7` arrives with a body that uses **another** group's name in the same subject. Which code should be returned, and why is it not a `422`?

Answer: `409 Conflict`. The body is **well formed**: every field has the correct type and length, so the model's validation passes. The problem is that the result would **conflict with the system's current state** (a group with that name already exists in that subject). `422` is for malformed data or data that breaks the rules of the format itself, and `409` is for a valid request that cannot be accepted right now.

## // Module summary

- [ ] I can implement `POST` returning `201` and the `Location` header.
- [ ] I can implement `PUT` (replace) and `PATCH` (change part).
- [ ] I can implement `DELETE` returning `204` with no body.
- [ ] I can apply business rules with `422` and `409`.
- [ ] I know why the identifier comes from a counter, not from `len(...)`.
- [ ] I know each route's success code and possible errors.

---

**Next module:** `12-swagger-in-practice.md`: the API is complete. What is left is learning to document it and to use Swagger as a real testing tool.

`Study Material // Coffee & Code`
