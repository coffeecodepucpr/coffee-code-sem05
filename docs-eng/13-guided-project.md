# Module 13, Guided Project: The Study Group API

[Português](../docs/13-projeto-guiado.md) · English

`WEEK 05 // Central RESTful API`

---

## // What this module is for

No new concept shows up here. This module brings together, in order, everything Modules 01 to 12 taught, and ends with the week's deliverable: a local FastAPI API with the complete group CRUD, validation, correct status codes and documented Swagger.

## // Step 1, Prepare the folder and the environment (Module 05)

In the `api-grupos` folder, confirm the virtual environment exists and is **active** (the terminal shows `(.venv)`). Confirm the version with `python --version`: it needs to be 3.10 or higher.

## // Step 2, Install FastAPI (Module 07)

The `requirements.txt` file should have this line:

```
fastapi[standard]>=0.143,<0.144
```

```
pip install -r requirements.txt
fastapi --version
```

## // Step 3, The data (Modules 06 and 10)

Create `dados.py` with the six sample subjects and six sample groups, and `CONTADOR_GRUPOS` starting at 7. The full file is in `example/api-basica/dados.py`.

## // Step 4, The models (Module 09)

Create `schemas.py` with `MateriaOut`, `GrupoBase`, `GrupoCreate`, `GrupoUpdate`, `GrupoPatch` and `GrupoOut`. Check that it imports: `python -c "import schemas"`.

## // Step 5, The read routes (Module 10)

In `main.py`, create the application with `title`, `description` and `version`, and write `GET /materias`, `GET /materias/{materia_id}`, `GET /grupos` (with `q` and `materia_id`) and `GET /grupos/{grupo_id}`, using `buscar_grupo_ou_404`. Remove the example routes from Modules 07 and 08.

Start the server (`fastapi dev main.py`) and check in `/docs` that the four routes showed up.

## // Step 6, The write routes (Module 11)

Write the `conferir_materia` and `conferir_nome_livre` functions, and the routes `POST /grupos` (201 and `Location`), `PUT /grupos/{grupo_id}`, `PATCH /grupos/{grupo_id}` and `DELETE /grupos/{grupo_id}` (204).

## // Step 7, The documentation (Module 12)

Add a `summary` to every route, `openapi_tags` with the description of `materias` and `grupos`, and `responses` on the routes that can return `404`, `409` or `422`.

## // Step 8, The test script

In Swagger, run these 17 requests, **in this order**, and check the expected result. All the results below were obtained from the running API.

| # | Request | Expected result |
|---|---|---|
| 1 | `GET /grupos` | `200`, six groups |
| 2 | `GET /grupos?q=prática` | `200`, only `Estruturas na prática` |
| 3 | `GET /grupos?materia_id=1` | `200`, only `Cálculo passo a passo` |
| 4 | `GET /grupos/3` | `200`, the `Modelagem e SQL` group |
| 5 | `GET /grupos/99` | `404`, `Grupo não encontrado` |
| 6 | `GET /grupos/abc` | `422`, `int_parsing`, with `loc` pointing to `path` and `grupo_id` |
| 7 | `POST /grupos` with `Cálculo II na prática`, subject 1, limit 5 | `201`, `grupo_id` 7, header `Location: /grupos/7` |
| 8 | The same `POST` again | `409`, `Já existe um grupo com esse nome nessa matéria` |
| 9 | `POST /grupos` with `materia_id` 99 | `422`, `A matéria 99 não existe` |
| 10 | `POST /grupos` with `nome_grupo` equal to `ab` | `422`, `string_too_short` |
| 11 | `PUT /grupos/7` with `Cálculo II revisado`, subject 1, limit 6 | `200`, the replaced group |
| 12 | `PATCH /grupos/7` with `max_participantes` 8 | `200`, only the limit changed |
| 13 | `PATCH /grupos/7` with `nome_grupo` equal to `null` | `422`, `loc` pointing to `body` and `nome_grupo` |
| 14 | `DELETE /grupos/7` | `204`, no body |
| 15 | `DELETE /grupos/7` again | `404` |
| 16 | `DELETE /grupos` | `405 Method Not Allowed` |
| 17 | `GET /materias/99` | `404`, `Matéria não encontrada` |

If all 17 match, the API is correct.

> **THE DATA GOES BACK TO THE START**
> In `fastapi dev` mode, the server restarts every time you **save a file**, and on each restart the data goes back to its initial state. That is expected, because everything lives in memory. If a test depends on a group you created, do the creation and the test before editing any file.

## // Step 9, Wrapping up the project

1. Run `pip freeze` and check that the versions match the installation (`requirements.txt` pins only FastAPI's range).
2. In the `README.md`, describe in a few lines: what the API does, how to install it (`pip install -r requirements.txt`), how to run it (`fastapi dev main.py`) and where the documentation is (`/docs`).
3. Confirm the `.venv` folder is kept out of the repository (`.gitignore`), if you use Git.
4. If you version the project with Git, make a commit: `git commit -m "Finish the study group API"`.

## // Wrap-up checklist

- [ ] The API starts with `fastapi dev main.py` without any error in the terminal.
- [ ] The 8 routes exist and show up in `/docs`, grouped by `materias` and `grupos`.
- [ ] The 17 requests in the script return the expected result.
- [ ] The status codes are correct: `201` on `POST`, `204` on `DELETE`, `404`, `409` and `422` on errors.
- [ ] Every route has a `summary`, and the ones that can fail have `responses`.
- [ ] `requirements.txt` pins FastAPI's version range.
- [ ] The `README.md` explains how to install and run.

## // Common mistakes when putting it all together

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `ModuleNotFoundError: No module named 'dados'` | The `dados.py` file is not in the same folder as `main.py`, or the server was started in another folder | Run `fastapi dev main.py` in the folder that contains both files |
| `ImportError` when importing from `schemas` | A model was typed wrong, or is missing from the file | Check the names imported in `main.py` |
| A route in the script returns `200` where `201` was expected | `status_code` is missing in the decorator | Check the `status_code` of `POST` and `DELETE` |
| `422` on every `POST`, `PUT` or `PATCH` with `curl` | The `Content-Type` is missing | Add `-H "Content-Type: application/json"` |
| The created group "disappeared" | The server restarted when a file was saved | That is expected: the data lives in memory |
| The `/grupos/novo` route (if created) is never reached | The route with a parameter was declared before it | Declare fixed routes before routes with parameters |

## // Applying it to the week's project

This is the application: there is no separate activity. By the end of this module, the API should pass the checklist in `deliverable.md`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> If you had to explain to someone, in three sentences, the path of a `POST /grupos` from the request to the response, what would you say?

Possible answer: FastAPI reads the JSON body, checks the `Content-Type` and validates the fields with the `GrupoCreate` model; if something is wrong, it returns `422` without even calling the function. If everything is right, the function checks the business rules (does the subject exist? is the name free?), generates the identifier, stores the group and returns `201` with the group and the `Location` header. At any point where a rule fails, the `HTTPException` stops the function and becomes a response with the right code.

## // Module summary

- [ ] I can repeat, from memory, the sequence of steps used to put the API together.
- [ ] My API passes the 17 requests in the test script.
- [ ] The wrap-up checklist is complete.

---

**Next module:** `14-organizing-an-api-in-layers.md` for the experienced track, or `deliverable.md` for the final review if you are following the main track.

`Study Material // Coffee & Code`
