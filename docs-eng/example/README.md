# Runnable examples, Week 05

[Português](../../docs/example/README.md) · English

This folder gathers everything that can be run this week. It is a reference, not a required answer key: your API needs to apply the same concepts, not be identical to this one.

> The code lives in [`docs/example/`](../../docs/example/), and its names, messages and comments are in Portuguese, the same as the rest of the track.

## Environment where everything was tested

| Item | Version |
|---|---|
| Python | 3.12.3 (FastAPI requires 3.10 or higher) |
| FastAPI | 0.143.0 |
| Starlette | 1.7.0 |
| Pydantic | 2.13.5 |
| Uvicorn | 0.54.0 |
| pytest | 9.1.1 |
| httpx2 | 2.13.1 |
| System | Linux. **Not tested on Windows or macOS** |

The official FastAPI documentation was checked on **October 8, 2026**. FastAPI is a `0.x` library and changes often: if something differs from what is here, the official documentation is the reference.

## Which folder to use

| Folder | Modules | What it is |
|---|---|---|
| `api-basica/` | 07 to 13 | The main track's API: three files |
| `api-em-pacotes/` | 14 | The same API split into packages and routers. The rules still import FastAPI |
| `api-limpa/` | 15 to 18 | Clean Architecture, global error handling, pagination and 36 tests |

All three behave the same for the client, with one difference: `api-limpa` returns **all** errors in the single `erro`, `mensagem` and `detalhes` format (Module 16), while `api-basica` and `api-em-pacotes` use FastAPI's default format (`detail`).

## `api-basica/`: the main track

```
api-basica/
├── main.py
├── dados.py
├── schemas.py
└── requirements.txt
```

To run it, inside the `api-basica` folder:

```
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py
```

The documentation opens at `http://127.0.0.1:8000/docs`. Use `fastapi dev`, not `fastapi run`: `dev` only serves your own computer, and `run` serves the whole network.

## `api-em-pacotes/`: Module 14

```
api-em-pacotes/
├── app/
│   ├── main.py
│   ├── dados.py
│   ├── schemas.py
│   ├── regras.py
│   └── routers/
│       ├── grupos.py
│       └── materias.py
└── requirements.txt
```

To run it, inside the `api-em-pacotes` folder: the same commands, replacing the last one with `fastapi dev app/main.py`.

## `api-limpa/`: Modules 15 to 18

```
api-limpa/
├── app/
│   ├── main.py
│   ├── dominio/            entities, errors and repository interfaces
│   ├── aplicacao/          the use cases
│   ├── infraestrutura/     the in-memory repository
│   └── api/                routes, models, dependencies and error handling
├── tests/                  36 tests
├── pytest.ini
└── requirements.txt
```

To run it, inside the `api-limpa` folder:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
pytest -q
```

## `curl-examples.md`

The `curl` requests used in the modules, with the real responses from a run of `api-basica`. Run them in order. See [curl-examples.md](curl-examples.md).

## Security rules

- Always run the API with `fastapi dev`. It has no access control.
- The virtual environment (`.venv`) never goes into the repository.
- The data lives in memory and goes back to its initial state on every server restart.
