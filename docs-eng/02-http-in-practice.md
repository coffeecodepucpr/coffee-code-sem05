# Module 02, HTTP in Practice

[Português](../docs/02-http-na-pratica.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

In Module 01 you saw that client and server talk through requests and responses. This module opens up that conversation and shows what it looks like inside. Knowing how to read a request and a response is what lets you, later on, understand error messages and debug the API with confidence.

## // The problem: what exactly travels over the network?

When you open a page or call an API, something is sent and something comes back. Without seeing that "something", any error looks like magic. The good news is that HTTP is a **text** protocol, readable by people.

## // What HTTP is

> **HTTP: IN SIMPLE WORDS**
> It is the protocol, that is, the set of conversation rules, used between browsers, apps and servers on the web. It works by **request and response**: the client sends a **request**, and the server sends back a **response**.

<div align="center">
<img src="../docs/assets/requisicao-resposta-http.svg" alt="The client sends an HTTP request to the server and receives an HTTP response" width="640">
</div>

Each request gets exactly one response. When the server responds, the conversation for that request ends.

## // Anatomy of a request

This is a request to create a group, written the way it travels over the network:

```
POST /grupos HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Content-Length: 58

{"nome_grupo": "Cálculo II na prática", "materia_id": 1}
```

<div align="center">
<img src="../docs/assets/anatomia-requisicao.svg" alt="An HTTP request split into start line, headers and body" width="640">
</div>

| Part | What it contains | In the example |
|---|---|---|
| **Start line** | The method, the path and the HTTP version | `POST /grupos HTTP/1.1` |
| **Headers** | Information about the request, one per line, in the format `Name: value` | `Content-Type: application/json` |
| **Blank line** | Separates the headers from the body | (empty) |
| **Body** | The data sent, when there is any | The group's JSON |

Not every request has a body. A `GET` that only reads data usually goes with just the start line and the headers.

## // Anatomy of a response

This is the real response this week's API sends back to the request above (the server also sends the `date` header, left out here to keep it short):

```
HTTP/1.1 201 Created
server: uvicorn
content-length: 149
content-type: application/json
location: /grupos/7

{"nome_grupo":"Cálculo II na prática","materia_id":1,"max_participantes":5,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

<div align="center">
<img src="../docs/assets/anatomia-resposta.svg" alt="An HTTP response split into status line, headers and body" width="640">
</div>

| Part | What it contains | In the example |
|---|---|---|
| **Status line** | The version, the **status code** and the phrase describing it | `HTTP/1.1 201 Created` |
| **Headers** | Information about the response | `location: /grupos/7` |
| **Body** | The data returned, when there is any | The newly created group, in JSON |

The status code is what tells you, before anything else, whether the request worked. Module 04 is entirely about it.

## // The URL inside

```
http://127.0.0.1:8000/grupos?q=prática&materia_id=1
```

| Part | Value in the example | Meaning |
|---|---|---|
| Scheme | `http` | The protocol used |
| Host | `127.0.0.1` | The computer that answers. `127.0.0.1` (or `localhost`) is your own computer |
| Port | `8000` | The program's "entrance door" on that computer |
| Path | `/grupos` | The resource being looked for |
| Query string | `?q=prática&materia_id=1` | Extra parameters, in the format `name=value`, separated by `&` |

When you run the API on your computer, the host will always be `127.0.0.1` and the port will be `8000`, unless you choose another.

## // The headers you will run into

| Header | Who sends it | What it is for |
|---|---|---|
| `Content-Type` | Client and server | States the body's format. For JSON, it is `application/json` |
| `Content-Length` | Client and server | The body's size, in bytes |
| `Host` | Client | The destination server and port |
| `Location` | Server | The address of the newly created resource |
| `Allow` | Server | The methods a route accepts (shows up in 405 responses) |
| `Date` and `Server` | Server | The response date and the program that responded (here, `uvicorn`) |

## // How to send requests

| Tool | What it does well | Limitation |
|---|---|---|
| **Browser** | Sending a `GET` by typing the address | Does not send a body or other methods |
| **Swagger** (Module 07 onward) | Sending any method, by filling in forms | Only exists once the API is running |
| **curl** | Sending any method, from the terminal | Requires care with quotes and headers |
| **Browser developer tools** (F12 key, Network tab) | Seeing the requests a page already makes | Shows them, but does not easily create new requests |

`curl` accepts four options that cover almost everything this week:

| Option | Meaning |
|---|---|
| `-i` | Shows the response headers, in addition to the body |
| `-X METHOD` | Chooses the method (`-X POST`, `-X DELETE`) |
| `-H "Name: value"` | Adds a header |
| `-d 'text'` | Sets the request body |

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Cálculo II na prática", "materia_id": 1}'
```

> **WATCH OUT ON WINDOWS**
> In Windows PowerShell, `curl` is an alias for another command, and the real `curl` is called `curl.exe`. On top of that, the quotes inside the JSON usually need different handling from what is shown above. The commands in this material were run on Linux and **were not tested on Windows**. If you have trouble, use Swagger (Module 07 onward), which works the same on any system and does not need quotes.

> **THE MOST FORGOTTEN HEADER**
> When sending JSON, the client needs to state `Content-Type: application/json`. In current versions of FastAPI, a request with a JSON body **without this header** is rejected with code 422 and an unclear message ("Input should be a valid dictionary or object to extract fields from"). Swagger and `curl -d` with `-H` send the right header, but anyone who forgets the `-H` in `curl` falls into this trap.

## // Good example × bad example

**Bad example**: sending JSON without the header:

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -d '{"nome_grupo": "Sem cabecalho", "materia_id": 1}'
```

```
HTTP/1.1 422 Unprocessable Entity
{"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"Input should be a valid dictionary or object to extract fields from", ...}]}
```

The server does not know the body is JSON, and the error message does not mention the header.

**Good example**: stating the body's format:

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Cálculo II na prática", "materia_id": 1}'
```

The result is the `201 Created` shown in the section on responses.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| 422 when sending JSON with `curl` | `-H "Content-Type: application/json"` missing | Add the header |
| `curl: (7) Failed to connect` | The API is not running, or the port is different | Check whether the server is up and which port it uses |
| Trying to send a `POST` by typing the address in the browser | The browser only sends `GET` when opening an address | Use Swagger or `curl` |
| Confusing the path with the whole URL | The URL has several parts | The path is only the part that starts at the first `/` after the port |
| Forgetting quotes around a URL with `&` in the terminal | `&` has a special meaning in some terminals | Put the URL in quotes |

## // Guided practice

1. Open any website in the browser and press the **F12** key.
2. Open the **Network** tab and reload the page.
3. Click the first row in the list and look for: the **method**, the **status code**, the response's `Content-Type` and the size.
4. Repeat with another row in the list (an image or a style file) and compare the `Content-Type` values.

## // Practice on your own

> **CHALLENGE**
> Read the request below and answer: what is the method, the path, how many headers are there and what is the body?

```
PATCH /grupos/3 HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Content-Length: 25

{"max_participantes": 12}
```

## // Applying it to the week's project

1. In the `README.md` of the `api-grupos` folder, add a "What the requests look like" section.
2. In it, write, in the format of this section, a `POST /grupos` request with a JSON body for a group you make up, and the `201 Created` response you expect to get.
3. If you version the project with Git, make a commit: `git commit -m "Document a request and response example"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Why does a `POST` request with a JSON body need the `Content-Type: application/json` header? What would the server not know without it?

Answer: because the body arrives only as a sequence of characters, and the server has no way of guessing whether it is JSON, plain text, form data or something else. `Content-Type` says how to interpret it. Without it, FastAPI does not treat the body as JSON and validation fails with a 422.

## // Module summary

- [ ] I can explain what HTTP is and what a request and a response are.
- [ ] I can identify the parts of a request (start line, headers and body).
- [ ] I can identify the parts of a response (status line, headers and body).
- [ ] I can split a URL into scheme, host, port, path and query string.
- [ ] I know why `Content-Type: application/json` is required when sending JSON.

---

**Next module:** `03-http-methods.md`: the first word of a request is the method. It says which action you want to perform on the resource.

`Study Material // Coffee & Code`
