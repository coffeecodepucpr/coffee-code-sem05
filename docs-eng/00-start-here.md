# Module 00, Start Here

[Português](../docs/00-comece-aqui.md) · English

`WEEK 05 // Central RESTful API`

---

## // Welcome to Week 05

Picture the **Study Group Finder** (*Buscador de Grupos de Estudo*), an application where students look for study groups for each subject. On the screen there is a list of groups, a form to create a new group and a button to delete one. But where do these groups come from? Where are they stored while nobody has the screen open? And who makes sure a group is not created with an empty name, or deleted twice?

The answer is a program that sits between the screens and the data, receiving requests, applying the rules and sending back responses. That program is the **central API**, and this week you build its first version, from scratch, in Python.

## // What a central API is

> **CENTRAL API: IN SIMPLE WORDS**
> It is a program that is always running, receives requests over the network (using the HTTP protocol), applies the system's rules and sends back responses. It is "central" because it is the single point through which requests from any client pass: a web page, a mobile app or another program.

<div align="center">
<img src="../docs/assets/api-central-arquitetura.svg" alt="Several clients sending requests to the central API, which reads and changes the data and sends back responses" width="640">
</div>

The benefit of having a single point is that the rules live in one place only. If the rule "the group name must have at least 3 characters" were spread across every screen, it would only take one screen forgetting to apply it for the system to accept invalid data. In the central API, the rule exists once and applies to every client.

## // What you will build by the end of the week

- An API in **Python**, using the **FastAPI** framework, running on your own computer.
- The **CRUD** operations for study groups: list, fetch one, create, replace, update and delete. Plus reading the subjects.
- Automatic validation of incoming data, with clear error messages.
- Correct **status codes** in every situation: 200, 201, 204, 404, 409, 422.
- Interactive documentation, **Swagger**, which FastAPI generates on its own and where you test the API without writing any client.

## // What is still left out

> **NOT THIS WEEK YET**
> In this first part, the data stays **in memory**: it lives in Python variables and goes back to its initial state every time the server restarts. Also left out are the database, login and permissions, publishing the API on the internet, and any screen connected to it. This week is about building and understanding the API itself.

## // What you need to get started

- A computer with Windows, macOS or Linux, and permission to install programs.
- A text or code editor (any one works) and a terminal.
- A browser.
- An internet connection, to install packages and for the documentation page to load (Module 07 explains why).
- **No prior knowledge** of Python, HTTP or APIs. Everything is introduced from scratch, and this week does not depend on any other.

## // The two tracks

**If you are just starting**, you have never written an API. The main path assumes this: Modules 01 to 13 introduce each concept before it is needed, focusing on basic CRUD routes and Swagger.

**If you already have experience**, you have built some API before or know another language. Modules 14 to 16, clearly identified as the experienced track and placed after the essentials, cover organizing the API in layers, Clean Architecture and global error handling. Modules 17 and 18 are bonuses in the same track: automated tests, and filtering, sorting and pagination.

Both tracks build the same API. What changes between them is the depth.

## // Map of Week 05

| Module | Content | You will be able to |
|---|---|---|
| 01 | What a REST API is | Explain resources, routes and JSON |
| 02 | HTTP in practice | Read a request and a response |
| 03 | HTTP methods | Pick the right method for each action |
| 04 | Status codes | Pick the right code for each result |
| 05 | Python: environment, types and decisions | Set up the environment and write your first programs |
| 06 | Python: functions, lists and dictionaries | Organize data and logic in Python |
| 07 | Your first API with FastAPI | Run an API and open Swagger |
| 08 | Routes and parameters | Receive values through the URL, with validation |
| 09 | Models with Pydantic | Receive and return data with a guaranteed format |
| 10 | CRUD: reading data | Implement reading, with the 404 |
| 11 | CRUD: creating, updating and deleting | Implement writing, with 201, 204 and 409 |
| 12 | Swagger in practice | Document and test the API in the browser |
| 13 | Guided project | Have the complete API working |
| 14 | Organizing an API in layers (experienced) | Split the API into packages, routers and layers |
| 15 | Clean Architecture in FastAPI (experienced) | Keep the rules free from the framework |
| 16 | Global error handling (experienced) | Turn every error into a single format |
| 17 | Automated tests (experienced, bonus) | Test the API with `pytest` |
| 18 | Filtering, sorting and pagination (experienced, bonus) | Return large lists with control |

Each module is a standalone file, but they were written to be read in this order: the code only makes sense after you understand HTTP, and CRUD only makes sense after you understand the models.

> The example code keeps Portuguese names (`grupos` = groups, `materias` = subjects, `nome_grupo` = group name) so it matches the runnable examples in `docs/example/`.

---

**Next module:** `01-what-is-a-rest-api.md`: before writing any code, understand what an API is and why it follows a style called REST.

`Study Material // Coffee & Code`
