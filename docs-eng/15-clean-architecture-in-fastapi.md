# Module 15, Clean Architecture in FastAPI

[Português](../docs/15-clean-architecture-no-fastapi.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

> **EXPERIENCED TRACK**
> This module is part of the experienced track: it comes after the essential content and is not needed for the week's deliverable. Anyone following the main track can skip to `deliverable.md`.

Module 14 left a question: how do you make the **rules** layer stop knowing about FastAPI? This module answers with **Clean Architecture**: a way of organizing code so that the heart of the system, the rules, does not depend on any technology. The complete, tested API is in `example/api-limpa/`.

## // The problem: rules tied to the framework

In Module 14, the "group not found" rule raised an `HTTPException(404)`. That mixes two ideas that are not the same thing: **what went wrong** (the group does not exist) and **how to tell the client** (a `404` code in HTTP). The first idea belongs to the system. The second belongs to the web layer. When both live in the same place, changing one requires touching the other.

## // What Clean Architecture is

> **CLEAN ARCHITECTURE: IN SIMPLE WORDS**
> It is a way of organizing code in layers where **dependencies always point inward**: the outer layers (web, database) know the inner ones (the system's rules), but the inner ones **do not know** the outer ones. The core does not know FastAPI exists.

<div align="center">
<img src="../docs/assets/regra-da-dependencia.svg" alt="The project's four layers, with every import arrow pointing to the domain" width="640">
</div>

The project now has four layers:

| Layer | Folder | What it contains | Can import |
|---|---|---|---|
| **Domain** | `app/dominio` | Entities, domain errors and the repositories' **interfaces** | Only Python's standard library |
| **Application** | `app/aplicacao` | The use cases (`ServicoGrupos`, `ServicoMaterias`) | The domain |
| **Infrastructure** | `app/infraestrutura` | The in-memory repository | The domain |
| **API** | `app/api` | Routes, Pydantic models, error handling | The application and the domain. Only it knows FastAPI |

> **THE DEPENDENCY RULE**
> A file in one layer can only import from **more inner** layers. The domain imports nobody. This rule is what keeps the core free from frameworks.

The complete structure:

```
api-limpa/
├── app/
│   ├── main.py
│   ├── dominio/
│   │   ├── entidades.py
│   │   ├── erros.py
│   │   └── repositorios.py
│   ├── aplicacao/
│   │   └── servicos.py
│   ├── infraestrutura/
│   │   └── memoria.py
│   └── api/
│       ├── schemas.py
│       ├── dependencias.py
│       ├── erros.py
│       └── routers/
│           ├── grupos.py
│           └── materias.py
├── tests/
├── pytest.ini
└── requirements.txt
```

## // Domain: entities and errors

Entities are simple classes, with the concept's data and nothing else. Here, `@dataclass` (from the standard library) generates the constructor automatically:

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Grupo:
    grupo_id: int | None  # None while the group has not been stored yet
    nome_grupo: str
    materia_id: int
    max_participantes: int
    descricao: str | None
    criado_em: datetime
```

Domain errors say **what went wrong**, without a word about HTTP:

```python
class ErroDeDominio(Exception):
    """Base of all business rule errors."""

    codigo = "erro_de_dominio"

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class GrupoNaoEncontradoError(ErroDeDominio):
    codigo = "grupo_nao_encontrado"

    def __init__(self):
        super().__init__("Grupo não encontrado")
```

Notice: no `404`, no JSON, no `fastapi`. The rule now raises `GrupoNaoEncontradoError()`, and turning that into a `404` is another layer's job (Module 16 shows how).

## // The repository interface

How does the application store and fetch groups without knowing **where** they are? Through a repository's **interface**, defined in the domain itself:

```python
from typing import Protocol

from app.dominio.entidades import Grupo


class RepositorioGrupos(Protocol):
    def listar(self) -> list[Grupo]: ...

    def buscar(self, grupo_id: int) -> Grupo | None: ...

    def salvar(self, grupo: Grupo) -> Grupo:
        """Stores the group. If it has no identifier yet, creates one."""
        ...

    def apagar(self, grupo_id: int) -> None: ...
```

> **PROTOCOL: IN SIMPLE WORDS**
> It is a way of saying "any class that has these methods will do", without requiring it to inherit from anything. The interface describes **what** the core needs, and whoever implements it decides **how**.

The interface lives in the **domain**, and the implementation lives in the **infrastructure**. That is what inverts the dependency: the core dictates the contract, and the detail fits into it.

## // Application: the use cases

The service receives the repositories through its constructor, and only knows the interfaces:

```python
class ServicoGrupos:
    def __init__(self, grupos: RepositorioGrupos, materias: RepositorioMaterias):
        self._grupos = grupos
        self._materias = materias

    def buscar(self, grupo_id: int) -> Grupo:
        grupo = self._grupos.buscar(grupo_id)
        if grupo is None:
            raise GrupoNaoEncontradoError()
        return grupo

    def criar(self, nome_grupo: str, materia_id: int, max_participantes: int = 10, descricao: str | None = None) -> Grupo:
        self._conferir_materia(materia_id)
        self._conferir_nome_livre(nome_grupo, materia_id)
        novo = Grupo(None, nome_grupo, materia_id, max_participantes, descricao, datetime.now(timezone.utc))
        return self._grupos.salvar(novo)
```

The service imports nothing from `fastapi`, `pydantic` or `app.api`. It receives plain values and returns domain entities.

### > Changing without corrupting

Remember the `PATCH` that poisoned the data in Module 09? Here, the change rule is written so that a failure midway **never** leaves a group half changed:

```python
def alterar(self, grupo_id: int, **campos) -> Grupo:
    antigo = self.buscar(grupo_id)
    novo = replace(antigo, **campos)  # a NEW object: the old one is only replaced if everything works
    if "materia_id" in campos:
        self._conferir_materia(novo.materia_id)
    self._conferir_nome_livre(novo.nome_grupo, novo.materia_id, ignorar_id=grupo_id)
    return self._grupos.salvar(novo)
```

`replace` creates a **copy** with the changed fields. The checks run on the copy, and only at the end does the repository store the result. If any check fails, the original group was never touched.

## // Infrastructure: the detail that fits in

The in-memory repository implements the interface, without inheriting from anything:

```python
class RepositorioGruposEmMemoria:
    def __init__(self, grupos: list[Grupo]):
        self._grupos = {g.grupo_id: g for g in grupos}
        self._contador = itertools.count(max(self._grupos, default=0) + 1)

    def buscar(self, grupo_id: int) -> Grupo | None:
        return self._grupos.get(grupo_id)

    def salvar(self, grupo: Grupo) -> Grupo:
        if grupo.grupo_id is None:
            grupo = replace(grupo, grupo_id=next(self._contador))
        self._grupos[grupo.grupo_id] = grupo
        return grupo
    # listar and apagar, in the same style
```

If one day the groups are stored in a database, you would just write another class with the same four methods and swap it in **one** place. The application's rules would not change. (This week only the in-memory version exists: the database is a possibility, not something implemented.)

## // API: the only layer that knows FastAPI

The **composition root**, the place that chooses which repository to use and hands the service to the routes, lives in `app/api/dependencias.py`:

```python
_materias = novo_repositorio_de_materias()
_grupos = novo_repositorio_de_grupos()


def obter_servico_grupos() -> ServicoGrupos:
    return ServicoGrupos(_grupos, _materias)


ServicoGruposDep = Annotated[ServicoGrupos, Depends(obter_servico_grupos)]
```

And the routes become **thin**: they only translate HTTP into calls to the service and back.

```python
@router.get("/{grupo_id}", response_model=GrupoOut)
def buscar_grupo(grupo_id: int, servico: ServicoGruposDep):
    return servico.buscar(grupo_id)


@router.post("", response_model=GrupoOut, status_code=status.HTTP_201_CREATED)
def criar_grupo(novo: GrupoCreate, response: Response, servico: ServicoGruposDep):
    grupo = servico.criar(**novo.model_dump())
    response.headers["Location"] = f"/grupos/{grupo.grupo_id}"
    return grupo
```

No `if`, no rule, no `HTTPException`. The service returns an entity (`Grupo`, a dataclass), and `response_model=GrupoOut` converts it to JSON because the model has `ConfigDict(from_attributes=True)`, which tells Pydantic to read the object's attributes.

**Format** validation (a name with 3 to 60 characters, a limit of 2 to 50) stays at the edge, in Pydantic. **Business** rules (the subject exists, the name is free) stay in the core.

## // Proof that it works

### > 1. Testing the rules without HTTP and without FastAPI

Since the service only needs repositories, a test uses it directly, with no server, no request, no `TestClient`:

```python
def test_buscar_grupo_inexistente_levanta_erro_de_dominio(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(GrupoNaoEncontradoError):
        servico_grupos.buscar(99)


def test_alterar_que_falha_nao_corrompe_o_grupo(servicos):
    servico_grupos, _ = servicos
    servico_grupos.criar("Cálculo II na prática", materia_id=1)
    with pytest.raises(GrupoDuplicadoError):
        servico_grupos.alterar(1, nome_grupo="Cálculo II na prática")
    assert servico_grupos.buscar(1).nome_grupo == "Cálculo passo a passo"
```

The second test checks exactly the `PATCH` problem: the change fails, and the group stays intact.

### > 2. A test that protects the architecture

The dependency rule can be checked by a test that reads the files and looks for forbidden imports:

```python
def test_dominio_nao_importa_framework_nem_outras_camadas():
    assert _proibidos(_importacoes("dominio"), PROIBIDOS_NO_NUCLEO + ("app.aplicacao",)) == []
```

And to confirm the test **really catches** the error, the proof was done the other way around: the line `from fastapi import HTTPException` was deliberately added to `app/dominio/erros.py`, and the result was:

```
E       AssertionError: assert ['fastapi'] == []
tests/test_arquitetura.py:29: AssertionError
1 failed, 2 passed
```

With the line removed, the three architecture tests passed again. From now on, anyone who imports FastAPI inside the core sees the test fail.

## // The price of clean architecture

> **AN HONEST CONVERSATION**
> Compare: Module 13's API has 3 code files. The clean version has 11 (plus 6 empty `__init__.py` files) to do **exactly the same thing** from the client's point of view. For an API this size, that is more ceremony than necessary. Clean Architecture pays off when the system grows: when there are several ways to store data, complex rules, or many people working on different parts of the code. In a small, throwaway API, Module 13's simple version is the right choice. Knowing **when** to use each one is part of the skill.

## // Good example × bad example

**Bad example**: a rule that knows HTTP:

```python
# in app/aplicacao/servicos.py
from fastapi import HTTPException

def buscar(self, grupo_id):
    grupo = self._grupos.buscar(grupo_id)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
```

The architecture test fails, and the rule is tied to the framework again.

**Good example**: the rule raises an error from its own world:

```python
from app.dominio.erros import GrupoNaoEncontradoError

def buscar(self, grupo_id):
    grupo = self._grupos.buscar(grupo_id)
    if grupo is None:
        raise GrupoNaoEncontradoError()
```

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `ImportError` from a circular import | Two layers import each other | Follow the rule: only import from more inner layers |
| Pydantic models inside the domain | It is tempting to reuse `GrupoOut` as the entity | Use a `dataclass` in the domain, and convert at the edge with `from_attributes` |
| A status code inside a domain error | It seems handy to have the `404` ready | Leave the error without a status, and translate it in a single place (Module 16) |
| The route ended up with `if`s and rules | The code was written directly in the route out of habit | Move the logic to the service, and let the route only translate |
| The service creates its own repository | It seems simpler than receiving it | Receive the repository through the constructor: that is what allows swapping and testing |
| Understanding the architecture as "more folders" | The folders are what you see | The point is the **direction** of the dependencies: check it with the architecture test |

## // Guided practice

1. Open `example/api-limpa/` and identify which layer each file belongs to. Check that the imports follow the dependency rule.
2. Run `pytest -q` and read the tests in `test_servico_sem_fastapi.py`: none of them uses HTTP.
3. Do the mutation: add `from fastapi import HTTPException` to `app/dominio/erros.py`, run `pytest tests/test_arquitetura.py`, read the failure, and undo the change.
4. Pick a route (for example, `GET /materias/{materia_id}`) and follow its path through the four layers, from the `router` to the `repository`.

## // Practice on your own

> **CHALLENGE**
> Add a new use case, **counting a subject's groups**. Write the method `contar_por_materia(materia_id)` in `ServicoGrupos` (it should raise `MateriaInexistenteError` if the subject does not exist) and a route `GET /materias/{materia_id}/total-de-grupos`. Check that you only touched two places (the application and the route), and write a test for the method **without** using `TestClient`.

## // Applying it to the week's project

1. If you followed the experienced track, rewrite your API in layers, following the `api-limpa/` structure.
2. Copy `test_arquitetura.py` into your project and run it on every change.
3. If you version the project with Git, make a commit: `git commit -m "Reorganize the API with Clean Architecture"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Why does the `RepositorioGrupos` interface live in the **domain**, and the `RepositorioGruposEmMemoria` class in the **infrastructure**? What would change if the interface lived next to the implementation?

Answer: if the interface lived in the infrastructure, the service (in the application) would have to import it **from there**, and the dependency would point outward: the core would depend on the detail. With the interface in the domain, it is the core that **dictates the contract**, and the infrastructure that adapts to it. This inversion is what lets you swap memory for a database without touching the rules, and test the rules with a fake repository.

## // Module summary

- [ ] I can explain Clean Architecture and the dependency rule.
- [ ] I know the four layers (domain, application, infrastructure and API) and what each one can import.
- [ ] I can write an entity, a domain error and a repository interface.
- [ ] I know why the service receives the repository through its constructor.
- [ ] I can test the rules without HTTP and check the architecture with a test.
- [ ] I can recognize when this architecture is worth it, and when it is overkill.

---

**Next module:** `16-global-error-handling.md`: the rules now raise errors that do not know HTTP. One piece is missing: whoever turns those errors into responses.

`Study Material // Coffee & Code`
