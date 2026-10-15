# Module 09, Models with Pydantic

[Português](../docs/09-modelos-com-pydantic.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

URL parameters are for simple values, like a number or a word. But to create a group you need to send several fields at once, in JSON, in the request **body**. This module introduces Pydantic, the library FastAPI uses to describe and validate that data, and shows how FastAPI uses models both on the way in and on the way out.

## // The problem: data coming from outside cannot be trusted

Anyone can send anything: an empty name, a number where text is expected, a field too many or too few. Validating all of that by hand, field by field, creates dozens of repeated `if`s, and one forgotten check is enough for the system to accept invalid data. A **model** describes the expected format once, and validation happens on its own.

## // What a Pydantic model is

> **MODEL: IN SIMPLE WORDS**
> It is a class that describes the fields of a piece of data, with each one's type and rules. When you create an object from it, Pydantic checks everything, converts what it can and rejects what does not fit.

```python
from pydantic import BaseModel, Field


class Grupo(BaseModel):
    nome_grupo: str = Field(min_length=3, max_length=60)
    materia_id: int = Field(gt=0)
    max_participantes: int = Field(default=10, ge=2, le=50)
    descricao: str | None = None
```

Each line inside the class declares a field. What each part means:

| Part | Meaning |
|---|---|
| `nome_grupo: str` | The `nome_grupo` field is text |
| `Field(min_length=3, max_length=60)` | The text has 3 to 60 characters |
| `Field(gt=0)` | The number is **g**reater **t**han 0 |
| `Field(default=10, ge=2, le=50)` | It is 10 if not provided, and must be between 2 (**g**reater or **e**qual) and 50 (**l**ess or **e**qual) |
| `descricao: str \| None = None` | Optional: it can be text or `None`, and is `None` by default |

## // Pydantic in action

```python
g = Grupo(nome_grupo="Modelagem e SQL", materia_id="3")
print(repr(g))
print(g.model_dump())
print(type(g.materia_id))
```

```
Grupo(nome_grupo='Modelagem e SQL', materia_id=3, max_participantes=10, descricao=None)
{'nome_grupo': 'Modelagem e SQL', 'materia_id': 3, 'max_participantes': 10, 'descricao': None}
<class 'int'>
```

Notice three things. `materia_id` arrived as the **text** `"3"` and became the **number** `3`: Pydantic converts when the conversion is safe. The fields not provided got their default value. And `.model_dump()` returns the model back as a regular dictionary.

Now, invalid data:

```python
Grupo(nome_grupo="ab", materia_id=0, max_participantes=99)
```

```
3 errors
   ('nome_grupo',) string_too_short | String should have at least 3 characters
   ('materia_id',) greater_than | Input should be greater than 0
   ('max_participantes',) less_than_equal | Input should be less than or equal to 50
```

Pydantic did not stop at the first problem: it **gathered all three errors** at once, each with the field and the reason. That is what becomes the API's `422` response.

## // Models in the request body

In FastAPI, you just declare a parameter of the model's type, and it is read from the **JSON body**:

```python
@app.post("/grupos")
def criar_grupo(novo: Grupo):
    return novo
```

Before calling your function, FastAPI: reads the body, checks the `Content-Type`, converts the JSON, validates each field and, if everything is right, hands you the ready object in `novo`. If something fails, your function **does not even run**: the client gets the `422`.

<div align="center">
<img src="../docs/assets/fluxo-validacao-pydantic.svg" alt="The JSON body goes through the model's validation; if valid, the function runs, otherwise the response is a 422" width="640">
</div>

A real request with a name that is too short, and the response FastAPI produces on its own:

```
POST /grupos   {"nome_grupo":"ab","materia_id":1}

422  {"detail":[{"type":"string_too_short","loc":["body","nome_grupo"],"msg":"String should have at least 3 characters","input":"ab","ctx":{"min_length":3}}]}
```

The `loc` field now starts with `body`, because the problem is in the body.

## // Several models for the same resource

In practice, a group shows up in **slightly different** formats depending on the situation:

| Situation | What changes | API model |
|---|---|---|
| Create (`POST`) | The person does not send the identifier or the date: the API generates them | `GrupoCreate` |
| Replace (`PUT`) | The required fields are sent again | `GrupoUpdate` |
| Change part (`PATCH`) | All fields are optional | `GrupoPatch` |
| Return to the client | Includes the identifier and the creation date | `GrupoOut` |

To avoid repeating the fields four times, the code uses **inheritance**: a base model with the common fields, and the others starting from it:

```python
class GrupoBase(BaseModel):
    nome_grupo: str = Field(min_length=3, max_length=60)
    materia_id: int = Field(gt=0)
    max_participantes: int = Field(default=10, ge=2, le=50)
    descricao: str | None = Field(default=None, max_length=200)


class GrupoCreate(GrupoBase):
    """POST body: what the person sends to create a group."""


class GrupoOut(GrupoBase):
    """What the API returns: the group's fields plus the ones it generates itself."""

    grupo_id: int
    criado_em: datetime
```

`GrupoOut` inherits the four fields from `GrupoBase` and adds `grupo_id` and `criado_em`. The project's complete model, with all four, is in the `schemas.py` file in the `example/api-basica` folder.

## // response_model: what goes out is validated too

On the way out, `response_model` works as a **filter**. It guarantees that only the model's fields go out, even if the function returns more:

```python
class GrupoOut(BaseModel):
    grupo_id: int
    nome_grupo: str


@app.get("/interno", response_model=GrupoOut)
def interno():
    return {"grupo_id": 1, "nome_grupo": "Cálculo", "codigo_interno": "segredo-123"}
```

```
GET /interno

{"grupo_id":1,"nome_grupo":"Cálculo"}
```

The `codigo_interno` field **did not leak**. This avoids a classic security mistake: accidentally returning data that should not go out, just because it was in the dictionary the function built.

## // PATCH and model_dump

For `PATCH`, all of the model's fields are optional, and the function needs to know **which ones were actually sent**. `model_dump(exclude_unset=True)` returns only those:

```python
print(Grupo(nome_grupo="Redes na unha", materia_id=5).model_dump(exclude_unset=True))
```

```
{'nome_grupo': 'Redes na unha', 'materia_id': 5}
```

The `max_participantes` and `descricao` fields were left out, because the person did not send them. Without `exclude_unset`, they would come with their default values and **overwrite** the group's data without anyone asking for it.

### > Omitting is not the same as sending null

In `PATCH`, all fields are optional, and that opens a trap: the client can **omit** a field (does not want to change it) or send it as `null`. These are different things. For `descricao`, `null` makes sense: it means "delete the description". But for `nome_grupo`, `materia_id` and `max_participantes`, `null` makes no sense, and accepting it **corrupts the data**.

In a test, an unprotected version returned `500` for `{"nome_grupo": null}` and for `{"max_participantes": null}`. Worse: the change had already been saved in memory before the error happened, so, from then on, even `GET /grupos` (the whole list) returned `500` to any client, until the server restarted. A single bad request poisoned the API.

The protection is a **validator** that rejects `null` only in the three fields that do not accept it:

```python
class GrupoPatch(BaseModel):
    nome_grupo: str | None = Field(default=None, min_length=3, max_length=60)
    materia_id: int | None = Field(default=None, gt=0)
    max_participantes: int | None = Field(default=None, ge=2, le=50)
    descricao: str | None = Field(default=None, max_length=200)

    @field_validator("nome_grupo", "materia_id", "max_participantes")
    @classmethod
    def nao_aceita_null(cls, valor):
        if valor is None:
            raise ValueError("este campo não aceita null: omita-o para não alterá-lo")
        return valor
```

The validator **does not run** for an omitted field (the default value is not validated), and runs only when the client sends the field explicitly. The result, with real responses (the message says "this field does not accept null: omit it to leave it unchanged"):

```
PATCH /grupos/1   {"nome_grupo": null}

422  {"detail":[{"type":"value_error","loc":["body","nome_grupo"],"msg":"Value error, este campo não aceita null: omita-o para não alterá-lo","input":null,"ctx":{"error":{}}}]}

PATCH /grupos/1   {"descricao": null}     ->  200, the description is deleted
PATCH /grupos/1   {}                      ->  200, nothing changes
```

## // Good example × bad example

**Bad example**: receiving a loose dictionary and validating by hand:

```python
@app.post("/grupos")
def criar_grupo(novo: dict):
    if "nome_grupo" not in novo or len(novo["nome_grupo"]) < 3:
        return {"erro": "nome inválido"}
    ...
```

The dictionary accepts anything, the validation covers only one field, the error comes back with `200`, and Swagger does not know how to describe the body's format.

**Good example**: a model that describes the body:

```python
@app.post("/grupos")
def criar_grupo(novo: GrupoCreate):
    ...
```

Validation is complete and automatic, the error is a detailed `422`, and Swagger shows the expected format and a fillable example.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `422` with `loc: ["body"]` and "Input should be a valid dictionary" | The body did not arrive as JSON (missing `Content-Type`), or it is not an object | Send `Content-Type: application/json` and an object in braces |
| `422` with `json_invalid` and "JSON decode error" | The JSON is malformed (quotes, a comma, a missing brace) | Check the JSON syntax |
| A required field "disappears" from the response | It is not in the `response_model` | Declare every field that should go out |
| `PATCH` erases fields that were not sent | `exclude_unset=True` is missing | Use `model_dump(exclude_unset=True)` |
| Forgetting `= None` on an optional field | Without a default value, the field becomes required | Write `field: str \| None = None` |
| Mixing up `str` and `int` when sending JSON | `"3"` and `3` are different things in JSON | Pydantic converts when it is safe, but prefer sending the right type |

## // Guided practice

1. In a `modelos_teste.py` file, create this section's `Grupo` model and test it with `Grupo(nome_grupo="Modelagem e SQL", materia_id="3")`.
2. Cause the three errors from the example, and read the messages.
3. Test `.model_dump()` and `.model_dump(exclude_unset=True)` with and without the `max_participantes` field.
4. In `main.py`, add a `POST /teste-grupo` route that receives the model and returns it. Test it in Swagger with a valid body and an invalid one.
5. Create `GrupoOut` with one field fewer than the returned dictionary, and confirm the extra field does not leak.

## // Practice on your own

> **CHALLENGE**
> Create a `Livro` (book) model with `titulo` (title, text of 1 to 100 characters), `ano` (year, an integer between 1450 and 2100) and `autor` (author, optional text). Create a `POST /livros` route that receives the model and returns the book with an extra `id` field, and use `response_model` to control the output. Test the `ano` boundary values and an empty `titulo`.

## // Applying it to the week's project

1. Create the `schemas.py` file in the `api-grupos` folder, with the models `MateriaOut`, `GrupoBase`, `GrupoCreate`, `GrupoUpdate`, `GrupoPatch` and `GrupoOut`, the way they appear in `example/api-basica/schemas.py`.
2. Check that the file imports without errors: `python -c "import schemas"`.
3. If you version the project with Git, make a commit: `git commit -m "Add the API's Pydantic models"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Why does the `GrupoOut` model have the `grupo_id` and `criado_em` fields, but `GrupoCreate` does not?

Answer: because whoever **creates** the group should not choose the identifier or the date: they are the API's responsibility, which guarantees the identifier is unique and that the date is the real moment of creation. If `GrupoCreate` accepted these fields, any client could forge an existing `grupo_id` or a fake date. `GrupoOut`, on the other hand, describes what the API **returns**, and there both fields are part of the response.

## // Module summary

- [ ] I can create a model with `BaseModel`, types and `Field`.
- [ ] I know Pydantic converts types when it is safe and gathers all errors at once.
- [ ] I can receive a JSON body by declaring a parameter of the model's type.
- [ ] I know why different models are used to create, replace, change and return.
- [ ] I can use inheritance to avoid repeating fields.
- [ ] I know what `response_model` guarantees on the way out.
- [ ] I can use `model_dump(exclude_unset=True)` for `PATCH`.

---

**Next module:** `10-crud-reading-data.md`: with the models ready, it is time to really implement the CRUD routes, starting with reading.

`Study Material // Coffee & Code`
