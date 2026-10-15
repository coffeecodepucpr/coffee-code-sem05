# Module 03, HTTP Methods

[Português](../docs/03-metodos-http.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

In Module 02 you saw that every request starts with a method, like `GET` or `POST`. This module explains what each method means, when to use each one, and two important properties they have: being **safe** and being **idempotent**.

## // The problem: the same address, different actions

The route `/grupos/3` represents a group. But what do you want to do with it? Read it? Change its data? Delete it? Putting the action inside the address (`/apagarGrupo/3`) creates the chaos Module 01 described. HTTP's solution is to keep the address fixed and use the **method** to state the action.

## // The five CRUD methods

> **CRUD: IN SIMPLE WORDS**
> It is the acronym for the four basic operations on any data: **C**reate, **R**ead, **U**pdate and **D**elete. Almost every API is, deep down, a CRUD over some resource.

<div align="center">
<img src="../docs/assets/crud-metodos-http.svg" alt="The CRUD operations linked to the HTTP methods and the project's routes" width="640">
</div>

| Operation | Method | What it is for | Has a body? |
|---|---|---|---|
| Read | `GET` | Get a resource or a collection | No |
| Create | `POST` | Create a new resource in the collection | Yes |
| Replace | `PUT` | Swap a whole resource for a new version | Yes |
| Change part | `PATCH` | Change only some fields of a resource | Yes |
| Delete | `DELETE` | Remove a resource | No |

> **FOR THOSE WHO ALREADY KNOW SQL (OPTIONAL)**
> If you already know databases, the correspondences are: `GET` matches `SELECT`, `POST` matches `INSERT`, `PUT` and `PATCH` match `UPDATE`, and `DELETE` matches `DELETE`. This week does not use a database, so this is just a comparison: nothing that follows depends on it.

## // Safe and idempotent

Two concepts set the methods apart, and understanding them avoids hard-to-find bugs.

> **SAFE: IN SIMPLE WORDS**
> A method is safe when it **does not change anything** on the server. Calling it is like window shopping: you can do it as much as you like, with no consequences.

> **IDEMPOTENT: IN SIMPLE WORDS**
> A method is idempotent when repeating the same request several times leaves the server in the **same state** as a single request. The final result does not change, even if the response does.

| Method | Safe? | Idempotent? |
|---|---|---|
| `GET` | Yes | Yes |
| `POST` | No | No |
| `PUT` | No | Yes |
| `PATCH` | No | Not guaranteed |
| `DELETE` | No | Yes |

Real examples from this week's API show the difference:

- **DELETE is idempotent.** Deleting group 7 once returns `204 No Content`. Deleting it again returns `404 Not Found`. The response changed, but the final state is the same both times: group 7 does not exist.
- **POST is not idempotent.** Sending the same `POST /grupos` twice tries to create two groups. In the project's API, a rule prevents the second one (`409 Conflict`), but without that rule two identical groups would be created.
- **GET is safe.** Calling `GET /grupos` a thousand times does not change any group.

## // PUT × PATCH: replace or change

Both change a resource that already exists, but in different ways.

- **PUT** sends the **whole** resource. Whatever is not sent goes back to its default value.
- **PATCH** sends **only the fields that change**. The rest stay as they were.

In the project's API, group 3 has `max_participantes` equal to 8 and a description. This `PATCH` changes only the limit:

```
PATCH /grupos/3
{"max_participantes": 12}
```

The name and the description stay intact. A `PUT` that sends only `nome_grupo` and `materia_id`, on the other hand, makes `max_participantes` go back to its default value (10) and the description become empty, because `PUT` replaces the whole group.

## // Good example × bad example

**Bad example**: deleting with `GET`:

```
GET /apagarGrupo?id=3
```

A `GET` should be safe. Browsers and programs that visit links automatically can repeat a `GET` without anyone noticing, and each visit would delete a group.

**Good example**: deleting with `DELETE`:

```
DELETE /grupos/3
```

The method makes the intent explicit, and no program fires a `DELETE` by accident when following a link.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Using `POST` for everything | It works and is easy to remember | Pick the method by meaning: reading is `GET`, deleting is `DELETE` |
| Changing data with `GET` | It can be done, so it seems valid | `GET` should be safe. Use `PUT`, `PATCH`, `POST` or `DELETE` |
| Mixing up `PUT` and `PATCH` | Both "update" | `PUT` sends everything and replaces, `PATCH` sends only what changes |
| Sending a body with a `GET` or `DELETE` | Sending the identifier in the body seems natural | The identifier goes in the route (`/grupos/3`), not in the body |
| Thinking repeating a `POST` is harmless | It seems like just "sending it again" | `POST` is not idempotent: repeating it can create duplicates |

## // Guided practice

1. Imagine a library with the resource `/livros` (books). Write the route and method to: list all books, see one book, register a book, replace all of a book's data, fix only a book's title, and remove a book.
2. For each operation, mark whether the method is safe and whether it is idempotent.
3. Check your guess from the Module 01 challenge (`/buscarMateria?id=2`, `/atualizarGrupo`, `/removerGrupo?id=5`): which methods would you choose now?

## // Practice on your own

> **CHALLENGE**
> A form's "Save" button sends a `POST` to create a group. The person, impatient, clicks it twice in a row. Describe what can happen on the server, and explain why using `PUT` on an address that already contains the group's identifier would avoid the problem.

## // Applying it to the week's project

1. In the `README.md`, complete the "Planned routes" table from Module 01 with new columns: **safe?** and **idempotent?**.
2. Add two lines explaining, in your own words, the difference between `PUT` and `PATCH` in the context of the `/grupos` resource.
3. If you version the project with Git, make a commit: `git commit -m "Document HTTP methods and their properties"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> A client calls `DELETE /grupos/5` and the response is `404 Not Found`, because the group had already been deleted by another request. Is that a problem for `DELETE`'s idempotence?

Answer: no. Idempotence is about the server's **final state**, not the response code. After the first call group 5 does not exist, and after the second it still does not exist, so the state is the same. The 404 only says that, this time, there was nothing to delete.

## // Module summary

- [ ] I know the five CRUD methods and what each one does.
- [ ] I know what it means for a method to be safe and to be idempotent.
- [ ] I can say which methods are safe and which are idempotent.
- [ ] I know the difference between `PUT` and `PATCH`.
- [ ] I know why data should not be changed with `GET`.

---

**Next module:** `04-status-codes.md`: the method says what you want to do. The status code says what happened.

`Study Material // Coffee & Code`
