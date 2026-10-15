# Challenges, Week 05

[Português](../docs/desafios.md) · English

Optional challenges, organized by the week's modules. None is required for the basic submission; see `deliverable.md` for what is required. Use these challenges if you finished the main modules and want to go further, or if you want to make the API more robust.

---

## // HTTP, methods and status codes (Modules 01 to 04)

**If you are just starting**
- Open the browser's developer tools (F12 key, Network tab) on three different websites and write down, for each one, three requests with the method, the status code and the `Content-Type`.
- Pick a system from your daily life (an online store, a social network) and write the REST routes for its main resources, with each one's methods and success codes.

**If you already have experience**
- Research the `429 Too Many Requests` code and explain in which situation an API should return it.
- Research the difference between `401 Unauthorized` and `403 Forbidden`, and write an example of each for the `/grupos` resource.

---

## // Python (Modules 05 and 06)

**If you are just starting**
- Write a function `agrupar_por_materia(grupos)` that receives the list of groups and returns a dictionary where the key is the `materia_id` and the value is the list of that subject's groups.
- Write a function that receives the `GRUPOS` dictionary and returns the group with the most participants, or `None` if the dictionary is empty.

**If you already have experience**
- Research the difference between `dict.get`, `dict.setdefault` and `collections.defaultdict`, and rewrite the `agrupar_por_materia` function with each one.
- Research what generic *type hints* are (`list[dict]`, `dict[int, dict]`) and add them to every function in `dados.py`.

---

## // FastAPI, routes and Pydantic (Modules 07 to 09)

**If you are just starting**
- Add a `GET /grupos/{grupo_id}/vagas` route that returns only a group's `max_participantes`, and `404` if it does not exist.
- Add a validation to the `GrupoBase` model that rejects names made only of spaces (tip: research Pydantic's `field_validator` decorator).

**If you already have experience**
- Research the difference between `response_model_exclude_unset` and `response_model_exclude_none`, and use one of them to hide `descricao` when it is `null`.
- Research how Pydantic handles extra fields sent in the body (`extra="forbid"`) and make `POST /grupos` reject unknown fields.

---

## // CRUD and Swagger (Modules 10 to 12)

**If you are just starting**
- Add `GET /materias/{materia_id}/grupos`, which returns a subject's groups (and `404` if the subject does not exist).
- Document every route with an example success response, using the `responses` parameter.

**If you already have experience**
- Research the decorator's `operation_id` parameter and rewrite the operation identifiers into more readable names.
- Research how to configure Swagger to load its files from your own server, without depending on the internet (FastAPI's documentation calls this static files for `/docs`), and evaluate how much work it takes.

---

## // Experienced track (Modules 14 to 18)

- Add a second repository to `api-limpa`, `RepositorioGruposEmArquivo`, that stores the groups in a JSON file, and swap one for the other **only** at the composition root (`dependencias.py`). Check that no file in `dominio/` or `aplicacao/` had to change.
- Write an architecture test that guarantees `aplicacao` does not import `infraestrutura`, and prove it works by doing the mutation (add the forbidden import and watch the test fail).
- Register a handler for an error you created yourself (for example, `LimiteExcedidoError`), and confirm the `erro`, `mensagem` and `detalhes` format is kept.
- Research what a *middleware* is in FastAPI and write one that logs the method, the path and the time of each request.
- Add a `min_vagas` filter to the listing and create a test for it.
- Research why `offset` pagination can skip or repeat items when the data changes between one page and the next, and what cursor pagination is.
- Research the **RFC 9457** format (*Problem Details for HTTP APIs*) and compare it with Module 16's single error format.

---

## // General challenge (everyone)

Write a `docs/decisoes.md` file with the five main design decisions of your API, each in two sentences: what you decided and why. Examples: why `PATCH` and `PUT` coexist, why a repeated name returns `409` and not `422`, why identifiers come from a counter. If you can justify each one without looking at the material, your API is at a good level.
