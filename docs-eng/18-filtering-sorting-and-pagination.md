# Module 18, Filtering, Sorting and Pagination

[Português](../docs/18-filtros-ordenacao-e-paginacao.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

> **EXPERIENCED TRACK, BONUS MODULE**
> This module is part of the experienced track and is a **bonus**: it is not needed for the week's deliverable. Anyone following the main track can skip to `deliverable.md`.

With six groups, returning the whole list is harmless. With six thousand, it is wasteful: the server builds a huge response, the network carries it, and whoever receives it only needs the first items. This module teaches you to return lists **in pieces**, in an order chosen by the client, using FastAPI's **dependencies**. The code is in `example/api-limpa/`.

## // The problem: the whole list, every time

A `GET /grupos` route that returns everything has three problems as the data grows: the response is slow, it takes up memory on the server and the client, and it forces the screen to show (or throw away) thousands of items. The standard solution is **pagination**.

## // Pagination with limit and offset

> **PAGINATION: IN SIMPLE WORDS**
> It means splitting a large list into pages. The client asks for one page at a time with two parameters: `limit` (how many items it wants) and `offset` (how many items to skip before starting).

| Request | Meaning |
|---|---|
| `?limit=2` | The first 2 items |
| `?limit=2&offset=2` | Skip 2 and bring 2: the second page |
| `?limit=2&offset=4` | Skip 4 and bring 2: the third page |

Page `n` of size `limit` starts at `offset = (n - 1) × limit`. A real example, with the list of six groups sorted by name:

```
GET /grupos?limit=2             ->  Cálculo passo a passo, Estruturas na prática
GET /grupos?limit=2&offset=2    ->  Modelagem e SQL, Processos e memória
GET /grupos?limit=2&offset=4    ->  Redes na unha, Requisitos e histórias
GET /grupos?limit=2&offset=10   ->  (empty list, and it is still a 200)
```

Asking for a page past the end is not an error: it is just an empty list.

## // Dependencies with Depends

> **DEPENDENCY: IN SIMPLE WORDS**
> It is a function FastAPI runs **before** your route, handing the result over as an argument. It is used to reuse a piece of logic (such as reading `limit` and `offset`) across several routes, without copying the code.

You already used a dependency in Module 15: `ServicoGruposDep` hands the service to the routes. The pagination and sorting ones live in the same file, `app/api/dependencias.py`:

```python
def paginacao(
    limit: Annotated[int, Query(ge=1, le=100, description="Quantos itens devolver")] = 10,
    offset: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
) -> dict:
    return {"limit": limit, "offset": offset}


Paginacao = Annotated[dict, Depends(paginacao)]
```

And the route receives the result as a regular parameter:

```python
@router.get("", response_model=list[GrupoOut], summary="Lista os grupos")
def listar_grupos(response: Response, servico: ServicoGruposDep, paginacao: Paginacao, ordenacao: Ordenacao, q: str | None = None, materia_id: int | None = None):
    ...
```

The `limit` and `offset` parameters **do not appear** in the route's signature: FastAPI reads them inside the dependency, validates them and hands over the ready dictionary. But, in `/docs`, they show up as the route's query parameters, because OpenAPI gathers the ones from every dependency.

### > Limits protect the API

See what `Query(ge=1, le=100)` and `Query(ge=0)` do in practice, with the real responses in Module 16's single error format:

```
GET /grupos?limit=0     ->  422  query.limit   Input should be greater than or equal to 1
GET /grupos?limit=101   ->  422  query.limit   Input should be less than or equal to 100
GET /grupos?offset=-1   ->  422  query.offset  Input should be greater than or equal to 0
```

The 100-item ceiling (`le=100`) keeps someone from asking for `limit=1000000` and overloading the server. **Every paginated API needs a ceiling.**

## // Sorting with allowed values

To choose the sorting field and direction, you use the `Literal` type, which accepts **only** the listed values:

```python
def ordenacao(
    ordenar_por: Annotated[Literal["nome_grupo", "max_participantes", "criado_em"], Query(description="Campo de ordenação")] = "nome_grupo",
    ordem: Annotated[Literal["asc", "desc"], Query(description="Sentido da ordenação")] = "asc",
) -> dict:
    return {"ordenar_por": ordenar_por, "ordem": ordem}
```

A value outside the list is rejected with a `422` that lists the valid options:

```
GET /grupos?ordenar_por=banana

422  query.ordenar_por   Input should be 'nome_grupo', 'max_participantes' or 'criado_em'
```

In OpenAPI, `Literal` becomes a list of allowed values (`enum`), and Swagger usually offers them as a list of options to choose from, instead of a free text field.

## // Where the logic lives: in the service

In Module 15's architecture, the route does **not** filter, sort or slice the list: it only passes the values to the service, which handles everything and returns **the page and the total**:

```python
def listar(self, q=None, materia_id=None, ordenar_por="nome_grupo", ordem="asc", limit=10, offset=0) -> tuple[list[Grupo], int]:
    """Returns the requested page and the total number of groups matching the filters."""
    grupos = self._grupos.listar()
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g.nome_grupo.lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g.materia_id == materia_id]
    chave = (lambda g: g.nome_grupo.lower()) if ordenar_por == "nome_grupo" else (lambda g: getattr(g, ordenar_por))
    grupos.sort(key=chave, reverse=ordem == "desc")
    return grupos[offset : offset + limit], len(grupos)
```

A `lambda` function is a small, nameless function: here, it says **by which value** to compare each group. For the name, it compares in lowercase, so that `"Redes"` and `"cálculo"` end up in real alphabetical order. Notice the `return`: the total (`len(grupos)`) is calculated **before** the slice (`grupos[offset : offset + limit]`).

## // The total number of items: the X-Total-Count header

Whoever receives a page needs to know **how many pages exist**. But the response is a list, and a list has no room for an extra number. The solution used here is to return the total in a **header**:

```python
grupos, total = servico.listar(q=q, materia_id=materia_id, ordenar_por=..., ordem=..., limit=..., offset=...)
response.headers["X-Total-Count"] = str(total)
return grupos
```

A real response, sorted in descending order by participant limit:

```
GET /grupos?limit=2&ordenar_por=max_participantes&ordem=desc

HTTP/1.1 200 OK
x-total-count: 6
[Modelagem e SQL (limit 8), Cálculo passo a passo (limit 6)]
```

The total is calculated **after the filter and before pagination**: with `?q=prática&limit=1`, the total is 1 (only one group matches the filter), not 6. It is the number the screen needs to draw "page 1 of N".

> **THE ALTERNATIVE: AN ENVELOPE**
> Another common approach is to return an object instead of the list, like `{"total": 6, "itens": [...]}`. It has the advantage of being visible in the body, and the disadvantage of changing the response format (whoever expected a list breaks). The header keeps the list as it is, which is why it was chosen here.

## // Good example × bad example

**Bad example**: paginating on the screen, after receiving everything:

```
GET /grupos        ->  10,000 groups, 4 MB of JSON
(the screen shows only the first 10 and throws the rest away)
```

**Good example**: asking only for the page you need:

```
GET /grupos?limit=10&offset=0   ->  10 groups
```

Doing the work on the server saves network, memory and time for every client.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| An empty page returns `404` | Confusing "page past the end" with "nonexistent resource" | Return `200` with an empty list |
| Asking for `limit=1000000` brings the server down | The `limit` has no ceiling | Use `Query(ge=1, le=100)` |
| Confusing `offset` with the page number | Both seem like "where to start" | `offset` counts skipped **items**: page `n` starts at `(n - 1) × limit` |
| Two items with the same sorting value swap places between requests | In many systems (databases, for example) the order between ties is not guaranteed. In this in-memory API it is stable, but the habit is worth it | Add a second fixed criterion, such as `grupo_id` |
| The total does not match the page | The total was calculated after slicing the list | Calculate `len(grupos)` **before** the slice |
| `422` when asking for a sort order | The value is not in the `Literal` | Use one of the values listed in the error message |

## // Guided practice

1. Open `app/api/dependencias.py` and read `paginacao` and `ordenacao`.
2. Run the API and test in Swagger: `limit=2` on the three pages, `ordenar_por=max_participantes&ordem=desc`, and the invalid values.
3. Open `ServicoGrupos.listar` and confirm where the total is calculated relative to the slice.
4. Run `pytest tests/test_listagem.py` and read the five tests.

## // Practice on your own

> **CHALLENGE**
> Add `materia_id` to the list of allowed `ordenar_por` values and implement the tie-breaker: when two groups have the same value in the chosen field, the one with the lower `grupo_id` comes first. Tip: the `chave` function can return a **tuple**, like `(getattr(g, campo), g.grupo_id)`. Write a test that confirms the order.

## // Applying it to the week's project

1. If you followed the experienced track, keep pagination and sorting in your layered API.
2. In the `README.md`, describe the `limit`, `offset`, `ordenar_por` and `ordem` parameters, and the `X-Total-Count` header.
3. If you version the project with Git, make a commit: `git commit -m "Add filtering, sorting and pagination"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Should `X-Total-Count` be 6 on `GET /grupos?q=prática&limit=1`? Or should it be another number?

Answer: it should be **1**, the number of groups matching the `q=prática` filter (only `Estruturas na prática`). The total is calculated after the filters and before pagination, because it is there for the screen to know how many pages exist **for that search**, not for the whole catalog. `limit=1` only affects how many items come in the body, not the total.

## // Module summary

- [ ] I know what pagination is and how `limit` and `offset` work.
- [ ] I can create a dependency with `Depends` and reuse it across several routes.
- [ ] I can validate `limit` and `offset` with `Query(ge=..., le=...)` and I know why the ceiling matters.
- [ ] I can restrict values with `Literal` and sort with `sort`.
- [ ] I can return the total number of items in a header, and I know what to calculate before the slice.
- [ ] I know why the listing logic lives in the service, not in the route.

---

**Next step:** `deliverable.md`, the final review of everything Week 05 asked for.

`Study Material // Coffee & Code`
