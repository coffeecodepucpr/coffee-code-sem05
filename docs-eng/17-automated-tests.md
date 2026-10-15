# Module 17, Automated Tests

[Português](../docs/17-testes-automatizados.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

> **EXPERIENCED TRACK, BONUS MODULE**
> This module is part of the experienced track and is a **bonus**: it goes deeper into what Module 15 already used, and it is not needed for the week's deliverable. Anyone following the main track can skip to `deliverable.md`.

In Module 13 you checked the API with a script of 17 requests made by hand. It works, but it is tiring, and nobody repeats 17 requests after every small change. This module replaces the script with **automated tests**: small programs that make the requests, check the responses and warn you if something broke. The tests are in `example/api-limpa/tests/`.

## // The problem: changing the code is scary

Without tests, every change carries a hidden risk: you change one rule and, without meaning to, break another. You only find out when someone complains. With tests, the answer comes in under a second, right in the terminal.

## // pytest and TestClient

> **PYTEST: IN SIMPLE WORDS**
> It is a tool that finds and runs test functions. Every file called `test_*.py` and every function called `test_*` is run automatically. A test passes if none of its checks (`assert`) fail.

> **TESTCLIENT: IN SIMPLE WORDS**
> It is a "fake client" FastAPI offers to call the API **without starting a server**. It makes the requests directly against the application's code, which is fast and does not depend on the network.

## // Installing

The clean version's `requirements.txt` has three lines:

```
fastapi[standard]>=0.143,<0.144
pytest
httpx2
```

`httpx2` deserves an explanation. FastAPI's `TestClient` needs an HTTP request library. With the `httpx` library (installed along with `fastapi[standard]`), the test runs, but Python emits this warning on every run:

```
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

The warning asks you to install `httpx2`. That is what was done: with it installed, the warning goes away and the tests pass normally.

## // The first test

In `tests/test_materias.py`:

```python
def test_lista_as_seis_materias(client):
    assert len(client.get("/materias").json()) == 6
```

A good test has three moments, known by the acronym **AAA**:

| Moment | Meaning |
|---|---|
| **Arrange** | The `client`, provided by the fixture (see below) |
| **Act** | `client.get("/materias")` |
| **Assert** | The `assert` |

The test's name is a **sentence** describing what is expected ("lists the six subjects"). When it fails, the name already says what broke. Run it with `pytest -q`.

## // Fixtures: preparing the ground

> **FIXTURE: IN SIMPLE WORDS**
> It is a function that prepares something the tests need (a client, clean data) and hands it to whoever asks. Any test that declares a parameter with the fixture's name receives it.

`tests/conftest.py` holds the shared fixtures:

```python
@pytest.fixture
def servicos():
    """The use cases, with new in-memory repositories: no HTTP, no FastAPI."""
    materias = novo_repositorio_de_materias()
    grupos = novo_repositorio_de_grupos()
    return ServicoGrupos(grupos, materias), ServicoMaterias(materias)


@pytest.fixture
def client(servicos):
    """An HTTP client whose services were swapped for versions with clean data."""
    servico_grupos, servico_materias = servicos
    app.dependency_overrides[dependencias.obter_servico_grupos] = lambda: servico_grupos
    app.dependency_overrides[dependencias.obter_servico_materias] = lambda: servico_materias
    yield TestClient(app)
    app.dependency_overrides.clear()
```

What each part does:

| Part | What it does |
|---|---|
| `@pytest.fixture` | Marks the function as a fixture |
| `def servicos()` | Creates **new repositories** for each test: no test inherits another's data |
| `app.dependency_overrides[...]` | Swaps, only during the test, the composition root's dependency for a version with clean data |
| `yield TestClient(app)` | Hands the client to the test, and the code after `yield` runs when the test ends |
| `.clear()` | Undoes the swaps, leaving the API as it was |

`dependency_overrides` is a FastAPI feature made precisely for tests. It is only possible because Module 15's architecture **hands** the service to the routes through `Depends`, instead of the routes creating it themselves.

## // The configuration

The `pytest.ini` file, at the project root:

```
[pytest]
pythonpath = .
testpaths = tests
```

`pythonpath = .` puts the project folder on the import path, which is why `from app import ...` works inside the tests. Without that line, a plain `pytest` command fails like this:

```
ImportError while loading conftest '.../tests/conftest.py'.
ModuleNotFoundError: No module named 'app'
```

## // Three kinds of tests

The clean API's suite has 36 tests, in six files, and each one answers a different question:

| File | Tests | The question it answers |
|---|---|---|
| `test_servico_sem_fastapi.py` | 7 | Do the **rules** work, without HTTP and without FastAPI? |
| `test_arquitetura.py` | 3 | Is the core still **free from the framework**? |
| `test_api_grupos.py` | 9 | Do the group **routes** return the right codes and bodies? |
| `test_erros.py` | 9 | Does every error come out in the **single format**? |
| `test_listagem.py` | 5 | Do **filtering, sorting and pagination** work? |
| `test_materias.py` | 3 | Do the **subject** routes work? |

### > Testing a rule, without HTTP

```python
def test_nome_repetido_na_mesma_materia_e_recusado_sem_diferenciar_maiusculas(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(GrupoDuplicadoError):
        servico_grupos.criar("CÁLCULO PASSO A PASSO", materia_id=1)
```

`pytest.raises` checks that the code **raises** the expected error. No request was made.

### > Testing a route

```python
def test_cria_um_grupo(client):
    resposta = client.post("/grupos", json=NOVO)
    assert resposta.status_code == 201
    assert resposta.headers["location"] == "/grupos/7"
    assert resposta.json()["grupo_id"] == 7
```

### > Testing a response with no body

```python
def test_delete_devolve_204_sem_corpo_e_depois_404(client):
    resposta = client.delete("/grupos/2")
    assert resposta.status_code == 204
    assert resposta.content == b""
    assert client.delete("/grupos/2").status_code == 404
```

### > Testing the PATCH with null bug

```python
def test_patch_com_null_nos_outros_campos_devolve_422_e_nao_corrompe(client):
    for campo in ("nome_grupo", "materia_id", "max_participantes"):
        resposta = client.patch("/grupos/1", json={campo: None})
        assert resposta.status_code == 422
        assert resposta.json()["detalhes"][0]["campo"] == f"body.{campo}"
    assert client.get("/grupos").status_code == 200  # the whole list is still healthy
    assert client.get("/grupos/1").json()["max_participantes"] == 6
```

This test is the "life insurance" for Module 09's problem: if someone ever removes the validator, it fails right away. It is a good example of why **every fixed bug becomes a test**.

### > Testing an unexpected error

```python
def test_erro_inesperado_vira_500_em_json_sem_vazar_detalhes():
    app_de_teste = FastAPI()
    registrar_tratadores(app_de_teste)

    @app_de_teste.get("/quebra")
    def quebra():
        raise RuntimeError("detalhe interno secreto")

    resposta = TestClient(app_de_teste, raise_server_exceptions=False).get("/quebra")
    assert resposta.status_code == 500
    assert resposta.json() == {"erro": "erro_interno", "mensagem": "Erro interno do servidor", "detalhes": None}
    assert "secreto" not in resposta.text
```

The test creates a **minimal application just for itself**, with a route that breaks on purpose, since the real API has none. Notice `raise_server_exceptions=False` (Module 16).

## // Running the suite

```
pytest -q
```

```
....................................                                     [100%]
36 passed in 0.22s
```

Thirty-six tests in under a quarter of a second. That is what replaces the 17 manual requests, and many more, on every change.

## // Reading a failure

A failing test is **useful information**, not a problem. Look at a test written with a wrong expectation on purpose (group 3 has a limit of 8, and the test expects 10):

```python
def test_grupo_3_tem_limite_10(client):
    resposta = client.get("/grupos/3")
    assert resposta.status_code == 200
    assert resposta.json()["max_participantes"] == 10
```

```
    def test_grupo_3_tem_limite_10(client):
        resposta = client.get("/grupos/3")
        assert resposta.status_code == 200
>       assert resposta.json()["max_participantes"] == 10
E       assert 8 == 10

tests/test_falha.py:4: AssertionError
FAILED tests/test_falha.py::test_grupo_3_tem_limite_10 - assert 8 == 10
1 failed in 0.03s
```

The `>` sign marks the line that failed, and `assert 8 == 10` shows the actual value (8) against the expected one (10). The question becomes: is the code wrong, or is the test? Here, the test.

## // Good example × bad example

**Bad example**: a test that depends on another having run before it:

```python
def test_cria_grupo(client):
    client.post("/grupos", json=NOVO)

def test_busca_o_grupo_criado(client):
    assert client.get("/grupos/7").status_code == 200   # only works if the previous test ran
```

**Good example**: each test creates what it needs:

```python
def test_busca_o_grupo_criado(client):
    client.post("/grupos", json=NOVO)
    assert client.get("/grupos/7").status_code == 200
```

Together with the fixture that creates new repositories, each test starts from scratch and can run on its own.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` when running `pytest` | `pythonpath = .` is missing from `pytest.ini` | Create `pytest.ini` as shown |
| A test passes alone and fails in the suite | It depends on data left by another test | Use the fixture with new repositories, and have each test create what it needs |
| The `StarletteDeprecationWarning` warning on every test | Only `httpx` is installed | Install `httpx2` |
| `pytest` does not find the tests | The file or function does not start with `test_` | Rename to `test_*.py` and `def test_...` |
| The `POST` test returns `422` even with the right body | `content=` was used instead of `json=` | Use `json=` to send JSON with the correct header |
| The `500` test raises the exception | `TestClient` re-raises unexpected errors | Use `raise_server_exceptions=False` |
| One test "interferes" with the next ones | `dependency_overrides` was not cleared | Use `yield` in the fixture and `.clear()` afterwards |

## // Guided practice

1. Install `pytest` and `httpx2`, and create `pytest.ini`, the `tests` folder and `conftest.py` with the two fixtures.
2. Write `test_materias.py` with the three subject tests and run `pytest -q`.
3. Write a rule test, without HTTP, using the `servicos` fixture.
4. Write the `POST` test with `201` and `Location`, and the `409` test when repeating it.
5. Cause a failure on purpose, read the message and fix it.

## // Practice on your own

> **CHALLENGE**
> Write three new tests: (a) `GET /grupos?materia_id=99` returns `200` with an empty list; (b) `PATCH /grupos/1` with **another** group's `nome_grupo` in the same subject returns `409` (first create a group in subject 1 to have the conflict); (c) `POST /grupos` with `max_participantes` equal to 51 returns `422` with the field `body.max_participantes`. Run the suite and confirm they all pass.

## // Applying it to the week's project

1. If you followed the experienced track, complete your API's `tests` folder with at least one test for each route and one for each rule.
2. Run `pytest -q` before every commit.
3. If you version the project with Git, make a commit: `git commit -m "Add automated tests for the API"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Why does the `servicos` fixture create **new** repositories for each test, instead of reusing the same ones?

Answer: because tests can create, change and delete groups. If they all used the same repository, whatever one test did would carry over to the next, and the result would depend on the **order** they run in. With new repositories, every test starts from the same initial state (six groups, six subjects), and can run on its own, in any order.

## // Module summary

- [ ] I know what an automated test is, and what `pytest` and `TestClient` do.
- [ ] I can write a test with arrange, act and assert.
- [ ] I can create fixtures, and use `dependency_overrides` to swap a dependency.
- [ ] I can configure `pytest.ini` with `pythonpath`.
- [ ] I can test rules without HTTP, routes, responses with no body and errors.
- [ ] I can turn a fixed bug into a test, and read a failure message.

---

**Next module:** `18-filtering-sorting-and-pagination.md`, the other bonus module in the experienced track.

`Study Material // Coffee & Code`
