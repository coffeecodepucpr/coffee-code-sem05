# Module 07, Your First API with FastAPI

[Português](../docs/07-sua-primeira-api-com-fastapi.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

It is time to see an API respond. In this module you install FastAPI, write two routes, start the server and open Swagger, the interactive documentation FastAPI generates on its own. Have the virtual environment from Module 05 at hand, **activated**.

> **VERSIONS AND DATE CHECKED**
> This material was verified by running **FastAPI 0.143.0**, **Pydantic 2.13.5**, **Starlette 1.7.0**, **Uvicorn 0.54.0** and **Python 3.12.3**. The official FastAPI documentation was checked on **October 8, 2026**. FastAPI is a `0.x` library and changes often (for example, the strict `Content-Type`, the 422 constant and the `httpx2` warning are recent changes). If something differs from what is here, the official documentation is the reference.

## // The problem: building a web server from scratch is a lot of work

Accepting connections, understanding HTTP, converting JSON, validating data and generating error messages are repetitive tasks, and getting any of them wrong creates security holes. A framework does all of this for you, and leaves you only what is specific to your system.

## // What FastAPI is

> **FASTAPI: IN SIMPLE WORDS**
> It is a framework (a set of ready-made tools) for building APIs in Python. It reads your code's **type hints** to automatically validate incoming data, and generates interactive API documentation on its own.

Three characteristics explain its popularity: it is quick to write, it validates data without extra code, and the documentation never gets out of date, because it comes from the code itself.

## // Installing

With the virtual environment active, create a `requirements.txt` file in the `api-grupos` folder, with one line:

```
fastapi[standard]>=0.143,<0.144
```

And install:

```
pip install -r requirements.txt
```

Two details worth explaining:

- The `[standard]` part asks for the full package: FastAPI along with the `uvicorn` server and the `fastapi` command-line tool. Without it, you would have only the library.
- The range `>=0.143,<0.144` **pins the version**. FastAPI is still a `0.x` library, and new versions can change behavior. This week's examples were run on 0.143.

Check the installation:

```
fastapi --version
```

```
FastAPI CLI version: 0.0.32
FastAPI Cloud CLI version: 0.26.0
```

> **IF THE TERMINAL COMPLAINS ABOUT THE BRACKETS**
> In some terminals, like `zsh` (the macOS default), a command typed as `pip install fastapi[standard]` fails because of the brackets. That is why `requirements.txt` is the safest path: the file does not have this problem. If you type the command directly, put the package in quotes.

## // The first API

Create the file `main.py` in the `api-grupos` folder:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def raiz():
    return {"mensagem": "Olá, API!"}


@app.get("/status")
def status_da_api():
    return {"status": "no ar"}
```

Five lines of logic, and it is already a complete API. What each part does:

<div align="center">
<img src="../docs/assets/anatomia-de-uma-rota.svg" alt="A FastAPI route split into decorator, path, function and return" width="640">
</div>

| Part | What it does |
|---|---|
| `app = FastAPI()` | Creates the application. The name `app` is a convention |
| `@app.get("/")` | The **decorator**: says the function right below handles `GET` requests to the path `/` |
| `def raiz():` | The function that runs when the request arrives |
| `return {...}` | What the function returns. FastAPI converts the dictionary into JSON |

A function with a decorator forms a **route**. The function's name (`raiz`, "root") is not visible to the client: what matters is the decorator's method and path.

## // Starting the server

In the project folder, with the environment active:

```
fastapi dev main.py
```

The terminal shows something like this (the start of the output; the icons the program draws were left out here):

```
Starting FastAPI in development mode

Using import string: main:app

Server started at http://127.0.0.1:8000
Documentation at http://127.0.0.1:8000/docs

Logs:

INFO:     Will watch for changes in these directories: ['/path/to/your/folder']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The program itself tells you where the server is (`http://127.0.0.1:8000`) and where the documentation is (`/docs`). The `fastapi dev` command is **development** mode: it reloads the server on its own every time you save the file. To stop the server, press **Ctrl+C** in the terminal.

> **FASTAPI DEV × FASTAPI RUN**
> There is also the `fastapi run` command, the **production** mode: it does not reload on its own and announces the server at `http://0.0.0.0:...`. The address `0.0.0.0` means "listen on all of the computer's networks", not just on the computer itself, so **other devices on your network can reach the API**. `fastapi dev`, on the other hand, listens on `127.0.0.1`, which only your own computer can reach. Since this week's API has no access control, always use `fastapi dev` while studying.

Open `http://127.0.0.1:8000` in the browser. The response:

```
{"mensagem":"Olá, API!"}
```

And, in the terminal, each incoming request produces a log line:

```
INFO:     127.0.0.1:PORT - "GET / HTTP/1.1" 200 OK
```

That line brings together everything you learned in Module 02: the method (`GET`), the path (`/`), the HTTP version and the status code (`200 OK`).

## // Swagger: documentation you can use

Open `http://127.0.0.1:8000/docs`. This page is **Swagger UI**, generated automatically from your code. It lists every route and lets you **test it without writing any client**:

1. Click the `GET /` route row to expand it.
2. Click the **Try it out** button.
3. Click **Execute**.
4. Scroll down to the **Server response** section: that is where the code (`200`), the response body and the headers appear.

> **SWAGGER NEEDS INTERNET**
> FastAPI builds the `/docs` page by loading Swagger UI's files from a public distribution address (`cdn.jsdelivr.net`). If your computer is **offline**, the API keeps working normally, but the `/docs` page opens blank. It is the most common mistake for people studying without internet. The steps above were described based on Swagger UI's documentation and the structure FastAPI generates; check the button names on your screen.

Three addresses are generated for free by FastAPI:

| Address | What it is |
|---|---|
| `/docs` | Swagger UI, interactive |
| `/redoc` | An alternative, read-only documentation |
| `/openapi.json` | The API's description in a standardized format (OpenAPI), which the two previous pages read |

## // Testing the second route

Nothing needs to be added: the `/status` route is already in the file. Call `http://127.0.0.1:8000/status` in the browser:

```
{"status":"no ar"}
```

Now change the `raiz` message to `"Olá, mundo!"`, save the file and reload the page. The terminal shows the server reloaded on its own, and the response already comes with the new text.

## // Good example × bad example

**Bad example**: naming the file after a library:

```
fastapi.py
```

```
ImportError: cannot import name 'FastAPI' from partially initialized module 'fastapi' (most likely due to a circular import)
```

Python looks in the current folder first. If your file is called `fastapi.py`, it tries to import **itself** when you write `from fastapi import FastAPI`.

**Good example**: a name that does not collide with any library:

```
main.py
```

Avoid naming your files `fastapi.py`, `pydantic.py`, `uvicorn.py` or `random.py`.

## // Common mistakes

All the messages below were obtained by running the commands.

| Mistake | What it says | Why it happens | How to fix it |
|---|---|---|---|
| `fastapi: command not found` | `bash: line 1: fastapi: command not found` | The virtual environment is not active | Activate the environment (`(.venv)` in the terminal) |
| File not found | `Path does not exist nao_existe.py` | The file name in the command is wrong, or you are in the wrong folder | Check the name and run the command in the file's folder |
| Port in use | `ERROR:    [Errno 98] Address already in use` | Another server is already using port 8000 | Stop the other server, or use `fastapi dev main.py --port 8001` |
| `ImportError ... partially initialized module 'fastapi'` | (see the bad example) | The file has the same name as the library | Rename the file |
| `/docs` opens blank | (no error message in the terminal) | No internet to load Swagger's files | Connect to the internet and reload |
| I changed the code and the response did not change | (no message) | The file was not saved, or the server was started without development mode | Save the file and confirm you used `fastapi dev` |

## // Guided practice

1. Create the `requirements.txt`, install, and run `fastapi --version`.
2. Create `main.py` with the two routes and start the server.
3. Open the `/` route in the browser and check the log line in the terminal.
4. Open `/docs`, use **Try it out** and **Execute** on the `/status` route, and read the response section.
5. Open `/redoc` and `/openapi.json` and compare them with what you saw in `/docs`.

## // Practice on your own

> **CHALLENGE**
> Add a third route, `GET /sobre` ("about"), that returns a dictionary with the API's name and version (for example, `{"api": "Buscador de Grupos de Estudo", "versao": "1.0.0"}`). Save, reload, and confirm it showed up on its own in `/docs`, without you writing any documentation.

## // Applying it to the week's project

1. Keep `main.py` with the `/` and `/status` routes: it will be the base for everything that comes next.
2. Confirm the server starts with `fastapi dev main.py` and that `/docs` opens.
3. If you version the project with Git, make a commit: `git commit -m "First API with FastAPI"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You put `@app.get("/sobre")` above a function called `informacoes`. Which address does the client use to call it, `/sobre` or `/informacoes`?

Answer: `/sobre`. The address and method come from the **decorator**, and the function name only serves to organize your code (and to name the operation in the documentation). The client never sees the name `informacoes`.

## // Module summary

- [ ] I know what FastAPI is and why the version is pinned in `requirements.txt`.
- [ ] I can install FastAPI and check the installation.
- [ ] I can write a route with a decorator, a function and a return.
- [ ] I can start the server with `fastapi dev` and stop it with Ctrl+C.
- [ ] I can open Swagger at `/docs` and run a route through it.
- [ ] I know the most common mistakes at this stage and how to fix them.

---

**Next module:** `08-routes-and-parameters.md`: the routes at this stage do not receive anything. Next, how to receive values through the URL, with automatic validation.

`Study Material // Coffee & Code`
