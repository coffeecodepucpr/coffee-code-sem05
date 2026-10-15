# Coffee & Code | WEEK 05 | Central RESTful API (Part 1: CRUD)

[Português](README.md) · English

```text
> module: sem-05
> topic: central restful api (crud)
> status: online
> coffee loaded
```

Material for **Week 05** of the Coffee & Code track, a technology club founded by Software Engineering students at PUCPR and open to anyone who wants to learn by building.

This week takes someone who has never built an API to a working CRUD API, validated and documented with Swagger: Python, FastAPI, HTTP methods and status codes.

> **A standalone week:** it does not require any other week of the club. Python, HTTP and the example project are introduced from scratch.

> **About the language:** the English material lives in [`docs-eng/`](docs-eng/), with the same structure as [`docs/`](docs/) (Portuguese); the READMEs have an English version with the `.en.md` suffix. The diagrams and the runnable examples' code (names, messages and comments) stay in Portuguese.

## Where to start

**[docs-eng/00-start-here.md](docs-eng/00-start-here.md)**: read this one first. It gives the week's overview and the idea of a central API.

Then follow the modules in order. Modules `01` to `13` make up the main track:

| # | Module | About |
|---|---|---|
| 01 | [What is a REST API](docs-eng/01-what-is-a-rest-api.md) | API, resource, JSON and the ideas of REST |
| 02 | [HTTP in practice](docs-eng/02-http-in-practice.md) | Request, response, URL and `Content-Type` |
| 03 | [HTTP methods](docs-eng/03-http-methods.md) | `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, safe and idempotent |
| 04 | [Status codes](docs-eng/04-status-codes.md) | The status families and the codes of a CRUD |
| 05 | [Python: environment, types and decisions](docs-eng/05-python-environment-types-and-decisions.md) | Virtual environment, types, `if` and loops |
| 06 | [Python: functions, lists and dictionaries](docs-eng/06-python-functions-lists-and-dictionaries.md) | Functions, lists, dictionaries and type hints |
| 07 | [Your first API with FastAPI](docs-eng/07-your-first-api-with-fastapi.md) | Installing, `fastapi dev` and Swagger |
| 08 | [Routes and parameters](docs-eng/08-routes-and-parameters.md) | Path and query parameters, validation |
| 09 | [Models with Pydantic](docs-eng/09-models-with-pydantic.md) | Models, request body and `response_model` |
| 10 | [CRUD: reading data](docs-eng/10-crud-reading-data.md) | `GET` for a list and for one item, and the 404 |
| 11 | [CRUD: creating, updating and deleting](docs-eng/11-crud-creating-updating-and-deleting.md) | `POST`, `PUT`, `PATCH` and `DELETE`, with 201, 204 and 409 |
| 12 | [Swagger in practice](docs-eng/12-swagger-in-practice.md) | OpenAPI, Swagger UI and how to document |
| 13 | [Guided project](docs-eng/13-guided-project.md) | The complete API, with a 17-test script |

Modules `14` to `16` are the **experienced track**, and modules `17` and `18` are bonuses in that track. They are all optional and can be read later:

| # | Module | About |
|---|---|---|
| 14 | [Organizing an API in layers](docs-eng/14-organizing-an-api-in-layers.md) | Packages, `APIRouter` and layers |
| 15 | [Clean Architecture in FastAPI](docs-eng/15-clean-architecture-in-fastapi.md) | Domain, application, infrastructure and API |
| 16 | [Global error handling](docs-eng/16-global-error-handling.md) | `exception_handler` and a single error format |
| 17 | [Automated tests](docs-eng/17-automated-tests.md) | Bonus: `pytest`, `TestClient` and fixtures |
| 18 | [Filtering, sorting and pagination](docs-eng/18-filtering-sorting-and-pagination.md) | Bonus: `Depends` and pagination |

And, to look up whenever you need:

- [Runnable examples](docs-eng/example/README.md): the three versions of the API, for reference
- [Challenges](docs-eng/challenges.md): optional, to go beyond what is asked
- [Deliverable](docs-eng/deliverable.md): final checklist before closing the week

## The runnable examples

The [`docs/example/`](docs/example/) folder has three versions of the Study Group Finder API:

- `api-basica/`: the main track's API.
- `api-em-pacotes/`: the experienced track's version, split into packages.
- `api-limpa/`: the version with Clean Architecture, global error handling and tests.

All of them were run, and the responses quoted in the modules come from those runs. See the [folder's README](docs-eng/example/README.md) to install and run them.

It is **reference material, not an answer key**: the example is there for you to see one possible solution when you get stuck, not to copy.

## The deliverable

At the end of Week 05, the repository of **your project** (not this one) should have an `api-grupos` folder with:

```text
api-grupos/
├── main.py
├── dados.py
├── schemas.py
├── requirements.txt
└── README.md         ← how to install and run
```

The API needs to run locally with `fastapi dev main.py`, have the 8 CRUD routes with the correct methods and status codes, validate the data with Pydantic and open the documentation at `/docs`.

The full checklist is in [docs-eng/deliverable.md](docs-eng/deliverable.md).

## Class submissions

There are no Week 05 submissions yet. Want to be the first? See [how to submit](entregas/README.en.md).

## Versions and date checked

Material verified with **FastAPI 0.143.0**, Pydantic 2.13.5, Starlette 1.7.0, Uvicorn 0.54.0 and Python 3.12.3. The official FastAPI documentation was checked on **October 8, 2026**. FastAPI is a `0.x` library and changes often: if something differs from what is here, the official documentation is the reference.

## Ongoing project

All modules use the club's same fictional project: the **Study Group Finder** (*Buscador de Grupos de Estudo*), an application where students look for study groups by subject. This week's API handles the groups and the subjects. If you have your own project, the reasoning in each module applies the same way: just change the name.

## How it works

Coffee & Code is **100% online**. Each module was written to be self-contained: you study at your own pace, and you can move ahead faster, go back to previous weeks and look things up during the project.

The weekly meetings, also online, are there to answer questions, review concepts, code together and show what you have built, **not to lecture** (Brasília time, UTC-3):

- **Wednesday**: 8:00 PM to 9:30 PM
- **Saturday**: 10:00 AM to 11:30 AM

Both cover the same content. Pick whichever fits your week best, and you do not need to stay on the call for the whole time.

## Stuck?

Bring a specific question to the meeting or to Discord. `"my route returns 422, I already checked the model and the request body"` usually gets solved much faster than `"my API doesn't work"`.

And remember: not knowing something is not a problem. Knowing how to research is part of the field.

## Diagrams

All the diagrams used in the modules are in [`docs/assets/`](docs/assets/), as SVG.

## Previous weeks

- [WEEK 01: Kickoff & Design System](https://github.com/coffeecodepucpr/coffee-code-sem01)
- [WEEK 02: Web Interface (Part 1: Layout)](https://github.com/coffeecodepucpr/coffee-code-sem02)
- [WEEK 03: Web Interface (Part 2: Interactivity)](https://github.com/coffeecodepucpr/coffee-code-sem03)
- [WEEK 04: Data Modeling](https://github.com/coffeecodepucpr/coffee-code-sem04)

Full track and upcoming weeks: [Coffee & Code profile](https://github.com/coffeecodepucpr)

---

```text
HTTP 418: I'm a teapot
> ready to code
```
