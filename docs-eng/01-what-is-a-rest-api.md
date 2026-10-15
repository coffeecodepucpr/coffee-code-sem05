# Module 01, What Is a REST API

[Português](../docs/01-o-que-e-uma-api-rest.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

This module has no code. It introduces the ideas that organize everything that comes next: what an API is, what a resource is, why routes have the shape they do, and what the word REST means. Understanding this now avoids the feeling of memorizing rules for no reason.

## // The problem: programs need to talk

A screen listing groups needs the groups' data. But the data does not live on the screen: it lives in another program, on another computer. For two programs to exchange information, they need to agree on **how** to ask and **how** to answer. If each system invents its own way, each new screen requires learning a new conversation. An API solves this by defining the conversation.

## // What an API is

> **API: IN SIMPLE WORDS**
> An *Application Programming Interface* is the set of requests a program accepts and the format of the responses it sends back. It is a program's "menu": it lists what you can order, without showing how the kitchen works.

Two words help describe who takes part in this conversation:

| Role | Who it is | In the project |
|---|---|---|
| **Client** | Whoever makes the request | The browser, Swagger, `curl`, a screen, another program |
| **Server** | Whoever receives the request and responds | The API you are going to build |

The client always starts the conversation. The server never "calls" the client on its own: it waits for a request, responds and goes back to waiting.

## // Resources: the "things" the API exposes

> **RESOURCE: IN SIMPLE WORDS**
> It is a "thing" in the system that has its own address and can be read or changed. In this week's project, the resources are study **groups** (`grupos`) and **subjects** (`materias`).

Every resource has an address, called a **URL** or **route**:

| Address | What it represents |
|---|---|
| `/grupos` | The collection of all groups |
| `/grupos/3` | The group with identifier 3 |
| `/materias` | The collection of all subjects |
| `/materias/1` | The subject with identifier 1 |

Notice the pattern: the resource name is **plural** (`/grupos`), and, to point to a specific item, you add the identifier after a slash.

## // JSON: the language of data

Data travels between client and server as text. The most common format is **JSON**:

```json
{
  "grupo_id": 3,
  "nome_grupo": "Modelagem e SQL",
  "materia_id": 3,
  "max_participantes": 8,
  "descricao": "Encontros online às terças e aos sábados"
}
```

> **JSON: IN SIMPLE WORDS**
> It is a text format for representing data. An object goes between braces, each piece of information is a `"name": value` pair, and pairs are separated by commas. Values can be text (in double quotes), numbers, `true` or `false`, `null`, lists (in square brackets) or other objects.

Almost every programming language can read and write JSON. That is why a client in any language can talk to an API written in Python.

## // What REST means

> **REST: IN SIMPLE WORDS**
> It is a style of designing APIs on top of HTTP, based on resources with their own address and on a small set of standardized actions. An API that follows the style is called *RESTful*.

REST is not a library or a technology: it is a set of ideas. The four that matter this week:

1. **Everything is a resource with an address.** The groups live at `/grupos`, not at an address like `/getAllGroups`.
2. **Actions are standardized.** Instead of inventing an address for each action, you use the same address with different **methods** (Module 03 goes into detail).
3. **The response says how it went.** Each response carries a **status code** saying whether it worked and, if it did not, whose fault it was (Module 04 goes into detail).
4. **Each request is independent.** The server does not "remember" the previous request. Everything it needs to respond comes inside the request itself.

## // The API you are going to build

By the end of the week, the project's API will have these routes:

| Operation | Method | Route |
|---|---|---|
| List the groups | `GET` | `/grupos` |
| Fetch a group | `GET` | `/grupos/{grupo_id}` |
| Create a group | `POST` | `/grupos` |
| Replace a group | `PUT` | `/grupos/{grupo_id}` |
| Change part of a group | `PATCH` | `/grupos/{grupo_id}` |
| Delete a group | `DELETE` | `/grupos/{grupo_id}` |
| List the subjects | `GET` | `/materias` |
| Fetch a subject | `GET` | `/materias/{materia_id}` |

Names in braces, like `{grupo_id}`, mark where the identifier goes. The methods and verbs will become clear in the next modules.

## // Good example × bad example

**Bad example**: one address per action, with the verb inside the name:

| Route | What it does |
|---|---|
| `/listarGrupos` | Lists |
| `/criarGrupo` | Creates |
| `/apagarGrupo?id=3` | Deletes |

With 20 resources and 5 actions each, you end up with 100 different addresses to memorize, and every new API invents its own.

**Good example**: one address per resource, and the action comes from the method:

| Route | Method | What it does |
|---|---|---|
| `/grupos` | `GET` | Lists |
| `/grupos` | `POST` | Creates |
| `/grupos/3` | `DELETE` | Deletes |

Anyone who already knows one REST API can guess a good part of another, because they all follow the same pattern.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Thinking an API is the same as a "website" | Both respond to addresses | A website returns pages for people; an API returns data for programs |
| Thinking REST is a technology you install | The name sounds like a tool | REST is a design style, and FastAPI is a tool that helps you follow it |
| Putting verbs in the route (`/criarGrupo`) | It is the most natural way to think | Use plural nouns and leave the action to the HTTP method |
| Expecting the server to "remember" the previous request | In a regular app, the screen keeps the state | In REST, every request carries everything the server needs |

## // Guided practice

1. Think of a system you know (a library, a store, a recipe app) and list three of its resources, always in the plural.
2. For each resource, write the collection route and the route for a specific item.
3. Write, in JSON, an example of an item from one of these resources, with at least four fields of different types (text, number, `true` or `false`, and `null`).

## // Practice on your own

> **CHALLENGE**
> Rewrite these routes following the REST pattern: `/buscarMateria?id=2`, `/atualizarGrupo`, `/removerGrupo?id=5`. For each one, also say which HTTP method would fit best, even without knowing all of them yet (Module 03 checks your guess).

## // Applying it to the week's project

1. Create a folder called `api-grupos` on your computer. It will hold the whole project for the week.
2. Inside it, create a `README.md` file with two sections: "What the project is" (one sentence) and "Planned routes" (the table in this section).
3. If you version the project with Git, make a commit: `git commit -m "Plan the API routes"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> A tutorial you found online suggests creating the route `/grupos/criar` to register a group. What problem does this design bring, and how does the REST pattern solve it?

Answer: the problem is that the verb "criar" (create) is inside the address. To delete, update or fetch, you would have to invent `/grupos/apagar`, `/grupos/atualizar` and so on, and each person would pick a different name. In the REST pattern, the address identifies only the resource (`/grupos`), and the action is given by the method: `POST /grupos` creates, `GET /grupos` lists, `DELETE /grupos/3` deletes.

## // Module summary

- [ ] I can explain what an API is and what the client and server roles are.
- [ ] I know what a resource is and how it gets an address.
- [ ] I can read and write a simple JSON object.
- [ ] I know the four ideas of the REST style.
- [ ] I know why routes use plural nouns, not verbs.

---

**Next module:** `02-http-in-practice.md`: the conversation between client and server happens through a protocol called HTTP. Time to see what it looks like inside.

`Study Material // Coffee & Code`
