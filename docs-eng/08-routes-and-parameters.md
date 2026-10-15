# Module 08, Routes and Parameters

[Português](../docs/08-rotas-e-parametros.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

In Module 07 you wrote routes that do not receive anything. A real API needs to receive values: which group? which search term? This module shows the two ways of sending values through the URL, **path** and **query** parameters, and one of FastAPI's biggest advantages: the automatic validation of those values.

## // The problem: every request is different

The route `/grupos/3` and the route `/grupos/5` ask for different things, but it would be absurd to write a function for each identifier. What you want is **one** function that receives the number as input. That is what parameters are for.

## // Path parameters

> **PATH PARAMETER: IN SIMPLE WORDS**
> It is a variable part of the route itself, marked with braces in the decorator. The value the client writes at that point in the URL reaches the function as an argument.

```python
@app.get("/saudacao/{nome}")
def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}!"}
```

```
GET /saudacao/Ana

{"mensagem":"Olá, Ana!"}
```

The name in braces in the decorator (`{nome}`) needs to be **the same** as the function parameter's name (`nome`). That is how FastAPI knows to connect one to the other.

## // The parameter's type validates the value

See the same mechanism with an integer:

```python
@app.get("/vagas/{total}")
def vagas(total: int, ocupadas: int = 0):
    return {"total": total, "ocupadas": ocupadas, "livres": total - ocupadas}
```

Two different requests:

```
GET /vagas/6
200  {"total":6,"ocupadas":0,"livres":6}

GET /vagas/abc
422  {"detail":[{"type":"int_parsing","loc":["path","total"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

You **did not write any validation**. The hint `total: int` was enough: FastAPI tried to convert `abc` into an integer, failed, and returned a `422` explaining the problem. Notice the `loc` field: it says **where** the error is (`path`, that is, in the path) and **which** parameter (`total`).

That is what Module 06 promised: Python does not check type hints, but FastAPI reads them and turns them into validation.

## // Query parameters

> **QUERY PARAMETER: IN SIMPLE WORDS**
> It is an optional value sent after the `?` in the URL, in the format `name=value`, with several separated by `&`. Any function parameter that is **not** in the route becomes a query parameter.

In the previous example, `ocupadas` does not appear in the route, so it is a query parameter:

```
GET /vagas/6?ocupadas=2
200  {"total":6,"ocupadas":2,"livres":4}

GET /vagas/6?ocupadas=x
422  {"detail":[{"type":"int_parsing","loc":["query","ocupadas"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"x"}]}
```

Now `loc` says `query`. The golden rule on when to use each type:

| Type | What for | Example |
|---|---|---|
| **Path** | Identify **which** resource | `/grupos/3` |
| **Query** | Filter, search, sort or paginate | `/grupos?q=sql&materia_id=3` |

### > Required or optional

| Declaration | Meaning |
|---|---|
| `ocupadas: int` | **Required**: a request without it returns 422 |
| `ocupadas: int = 0` | **Optional**, with default value `0` |
| `q: str \| None = None` | **Optional**, and is `None` when not sent |

## // Validating better with Query

To impose rules on the value (minimum and maximum length), use `Query`:

```python
from typing import Annotated
from fastapi import Query

@app.get("/buscar")
def buscar(q: Annotated[str | None, Query(min_length=2, max_length=30)] = None, limite: int = 10):
    return {"q": q, "limite": limite}
```

```
GET /buscar
200  {"q":null,"limite":10}

GET /buscar?q=sql&limite=5
200  {"q":"sql","limite":5}

GET /buscar?q=s
422  {"detail":[{"type":"string_too_short","loc":["query","q"],"msg":"String should have at least 2 characters","input":"s","ctx":{"min_length":2}}]}
```

`Annotated[...]` is the current way to attach rules to a type: it reads as "a string or `None`, with a length between 2 and 30".

## // Route order matters

When two routes could match the same address, FastAPI uses **the first one declared**:

```python
@app.get("/grupos/{grupo_id}")
def grupo_por_id(grupo_id: int):
    return {"grupo_id": grupo_id}

@app.get("/grupos/novo")
def tela_novo():
    return {"nunca": "chega aqui"}
```

```
GET /grupos/novo
422  {"detail":[{"type":"int_parsing","loc":["path","grupo_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"novo"}]}
```

The word `novo` ("new") matched `{grupo_id}` before reaching the fixed route, and the integer conversion failed. The solution is to declare **fixed** routes before routes with parameters.

## // Good example × bad example

**Bad example**: validating by hand what the type already validates:

```python
@app.get("/vagas/{total}")
def vagas(total):
    if not total.isdigit():
        return {"erro": "total precisa ser número"}
    ...
```

This code returns `200` with the error message (a problem Module 04 described), repeats work FastAPI already does, and even rejects values like `-3`, which the `int` type would accept.

**Good example**: letting the type do the work:

```python
@app.get("/vagas/{total}")
def vagas(total: int, ocupadas: int = 0):
    return {"total": total, "ocupadas": ocupadas, "livres": total - ocupadas}
```

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `422` when calling a "correct" route | The value does not match the declared type (`abc` where an `int` is expected) | Read the `loc` and `msg` fields: they tell you which parameter and which problem |
| The function parameter does not receive the value | The name in the route (`{grupo_id}`) is different from the name in the function | Use exactly the same name in both places |
| A query parameter is treated as required | It was declared without a default value | Give it a default (`= 0`, `= None`) to make it optional |
| A fixed route is never reached | A route with a parameter was declared before it | Declare fixed routes first |
| The `&` character breaks the URL in the terminal | `&` has a special meaning in some terminals | Put the URL in quotes |
| Accents turn into `%c3%a1` in the URL | A URL only accepts certain characters and encodes the rest | That is normal: the server decodes it back on its own |

## // Guided practice

1. In `main.py`, add the `/saudacao/{nome}` route and test it in the browser and in Swagger.
2. Add the `/vagas/{total}` route with the optional `ocupadas` parameter. Test it with and without it, and with invalid values.
3. Add the `/buscar` route with `q` validated by `Query`. Test `q` with 1 character.
4. Declare `/grupos/{grupo_id}` before `/grupos/novo`, test both addresses, then swap the order and test again.
5. In `/docs`, see how the parameters show up in each route's form.

## // Practice on your own

> **CHALLENGE**
> Write the route `GET /desconto/{preco}` that receives a price (a decimal number, `float`) and an optional query parameter `percentual` (an integer, defaulting to 10, with a value between 0 and 100, using `Query` with `ge` and `le`). The route should return the price, the percentage and the final price. Test invalid values for both parameters and read each error's `loc`.

## // Applying it to the week's project

1. Keep this module's example routes in `main.py` (they will be removed in Module 13, when the final API is put together).
2. Note in the `README.md` which of the final API's parameters will be **path** parameters and which will be **query** parameters: the group identifier, the search term and the subject filter.
3. If you version the project with Git, make a commit: `git commit -m "Add routes with parameters"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> In the route `GET /grupos/{grupo_id}`, the person calls `/grupos/-5`. The `int` type accepts negative numbers, so validation passes. What should your function do, and what code should the person get?

Answer: type validation only guarantees that `-5` is an integer. It is up to **your function** to look for a group with that identifier, find none, and return `404 Not Found`. In this week's API, `GET /grupos/-5` and `GET /grupos/0` return exactly that: `404` with `{"detail":"Grupo não encontrado"}`.

## // Module summary

- [ ] I can declare a path parameter and connect it to the function's argument.
- [ ] I know the parameter's type validates the value with no extra code.
- [ ] I can declare query parameters, required and optional.
- [ ] I know when to use a path parameter and when to use a query parameter.
- [ ] I can use `Query` to impose minimum and maximum length.
- [ ] I know fixed routes must come before routes with parameters.
- [ ] I can read the `loc` field of a 422 error.

---

**Next module:** `09-models-with-pydantic.md`: URL parameters are for simple values. To receive a whole group, in JSON, models come in.

`Study Material // Coffee & Code`
