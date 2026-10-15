# Module 06, Python: Functions, Lists and Dictionaries

[Português](../docs/06-python-funcoes-listas-e-dicionarios.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

In Module 05 you set up the environment and saw Python's basic building blocks. This module introduces the four tools the API uses all the time: functions, lists, dictionaries and type hints. When you open the API's code, almost everything you see will be a combination of them.

## // The problem: repeated logic and loose data

A program that repeats the same snippet five times is hard to maintain, and a program with data spread across dozens of variables is hard to understand. Functions solve the first problem, and lists and dictionaries solve the second.

## // Functions

> **FUNCTION: IN SIMPLE WORDS**
> It is a named block of code that receives input values (the **parameters**), does some work and can return a result with `return`. You write it once and use it as many times as needed.

```python
def descrever(nome_grupo, vagas=10):
    return f"{nome_grupo}: {vagas} vagas"

print(descrever("Modelagem e SQL", 8))
print(descrever("Redes na unha"))
print(descrever(vagas=4, nome_grupo="Processos e memória"))
```

```
Modelagem e SQL: 8 vagas
Redes na unha: 10 vagas
Processos e memória: 4 vagas
```

Three important points:

- `def` defines the function, and the body is indented, as in an `if`.
- `vagas=10` is a **default value**: if the call does not provide `vagas`, it is 10.
- Arguments can be passed **by name** (`vagas=4`), in any order. FastAPI uses this style a lot.

## // Lists

> **LIST: IN SIMPLE WORDS**
> It is an ordered sequence of values, written in square brackets. Each value has a position, and positions are counted starting from **zero**.

```python
materias = ["Cálculo I", "Estrutura de Dados", "Banco de Dados"]
materias.append("Redes")
print(len(materias), materias[0], materias[-1], materias[1:3])

longas = [m for m in materias if len(m) > 10]
print(longas)
```

```
4 Cálculo I Redes ['Estrutura de Dados', 'Banco de Dados']
['Estrutura de Dados', 'Banco de Dados']
```

| Operation | Result |
|---|---|
| `materias[0]` | The first item |
| `materias[-1]` | The last item |
| `materias[1:3]` | A slice: from position 1 to 2 (3 is not included) |
| `materias.append(x)` | Adds an item at the end |
| `len(materias)` | The number of items |

The second line of the example uses a **list comprehension**: `[m for m in materias if len(m) > 10]` reads as "a list with each `m` from the subjects, only if the length of `m` is greater than 10". It is the short and very common way to filter a list, and the API uses it to filter groups.

## // Dictionaries

> **DICTIONARY: IN SIMPLE WORDS**
> It is a collection of **key: value** pairs, written in braces. Instead of looking up by position, you look up by key. It is the structure that most resembles a JSON object.

```python
grupo = {"grupo_id": 3, "nome_grupo": "Modelagem e SQL", "descricao": None}
print(grupo["nome_grupo"], grupo.get("max"), grupo.get("max", 10))
print("grupo_id" in grupo, list(grupo.keys()))

grupo["max_participantes"] = 8
for chave, valor in grupo.items():
    print(chave, "->", valor)
```

```
Modelagem e SQL None 10
True ['grupo_id', 'nome_grupo', 'descricao']
grupo_id -> 3
nome_grupo -> Modelagem e SQL
descricao -> None
max_participantes -> 8
```

| Operation | Result |
|---|---|
| `grupo["nome_grupo"]` | The key's value. If the key does not exist, it raises an error (`KeyError`) |
| `grupo.get("max")` | The key's value, or `None` if it does not exist |
| `grupo.get("max", 10)` | The key's value, or `10` if it does not exist |
| `"grupo_id" in grupo` | `True` if the key exists |
| `grupo["nova"] = valor` | Creates or replaces a key |

### > Dictionaries of dictionaries: the format of the API's data

The API stores the groups in a dictionary whose key is the identifier and whose value is another dictionary with the group's data:

```python
grupos = {1: {"nome": "A"}, 2: {"nome": "B"}}
print(grupos.get(2), grupos.get(9))
print([g["nome"] for g in grupos.values()])
del grupos[1]
print(list(grupos))
```

```
{'nome': 'B'} None
['A', 'B']
[2]
```

Fetching a group by identifier is just `grupos.get(2)`. If it does not exist, the result is `None`, and the API uses that to decide whether to return a 404. `del` removes a key.

## // Automatic counter: next

To give each created group a new identifier, the API uses a **counter** from Python's standard library:

```python
import itertools
contador = itertools.count(7)
print(next(contador), next(contador), next(contador))
```

```
7 8 9
```

Each call to `next(contador)` returns the next number. The line `import itertools` brings into the program a library that already comes with Python.

## // Type hints

```python
def buscar(grupos, grupo_id: int) -> dict | None:
    return grupos.get(grupo_id)

print(buscar(grupos, 2), buscar(grupos, 99))
```

```
{'nome': 'B'} None
```

The pieces `: int` and `-> dict | None` are **type hints**. They say that `grupo_id` should be an integer and that the function returns a dictionary or `None`. The `|` symbol means "or".

> **TYPE HINTS DO NOT VALIDATE ANYTHING ON THEIR OWN**
> Python **does not check** type hints at runtime. A function declared with `x: int` accepts `"text"` without complaining. What FastAPI does is **read** these hints and turn them into automatic validation of the data reaching the API. That is the framework's big secret, and Module 08 shows it in action.

## // Errors and exceptions

When something goes wrong, Python stops the program and shows an **exception**. You can catch it and react:

```python
try:
    int("abc")
except ValueError as erro:
    print("erro:", erro)
```

```
erro: invalid literal for int() with base 10: 'abc'
```

FastAPI has its own way of turning exceptions into HTTP responses, which Module 10 introduces.

> **IF YOU ALREADY CODE IN ANOTHER LANGUAGE (OPTIONAL)**
> If you know JavaScript, Python's dictionary corresponds to the object literal, and the list corresponds to the *array*. The list comprehension plays the role of `.filter()` and `.map()`, and `try`/`except` corresponds to `try`/`catch`. If you do not know JavaScript, ignore this box.

## // Good example × bad example

**Bad example**: forgetting the `return`:

```python
def dobro(x):
    x * 2

print(dobro(4))
```

```
None
```

The calculation happens, but the result is thrown away. A function without `return` returns `None`.

**Good example**: returning the result:

```python
def dobro(x):
    return x * 2

print(dobro(4))
```

```
8
```

## // Common mistakes

| Mistake | What it says | Why it happens | How to fix it |
|---|---|---|---|
| `KeyError` | `KeyError: 'max'` | Accessing a key that does not exist with `grupo["max"]` | Use `grupo.get("max")` when the key may be missing |
| `IndexError` | `list index out of range` | Asking for a position the list does not have | Check the size with `len(lista)` |
| `TypeError` | `somar() missing 1 required positional argument: 'b'` | Calling a function with fewer arguments than it requires | Pass all the arguments, or define default values |
| The function returns `None` | (no message) | The `return` is missing | Add the `return` |
| Thinking `x: int` validates | (no message) | Python does not check type hints | Remember that validation comes from FastAPI and Pydantic |

## // Guided practice

1. Write a function `status_do_grupo(participantes, vagas)` that returns `"cheio"` (full), `"quase cheio"` (almost full) or `"com vagas"` (has spots).
2. Create a `grupo` dictionary with the keys `nome_grupo`, `materia_id` and `max_participantes`, and print each pair with a `for` and `.items()`.
3. Create a list with five group names and use a list comprehension to keep only those with more than 15 characters.
4. Create a dictionary of dictionaries with three groups, remove one with `del` and check the result with `.get()`.

## // Practice on your own

> **CHALLENGE**
> Create a `grupos` dictionary with three groups, where the key is the identifier. Write a function `buscar_grupo(grupos, grupo_id)` that returns the group, or `None` if it does not exist. Then write a function `listar_por_materia(grupos, materia_id)` that returns a **list** with only that subject's groups, using a list comprehension.

## // Applying it to the week's project

1. Inside the `api-grupos` folder, create the `dados.py` file.
2. In it, write a `MATERIAS` dictionary with 3 subjects (keys `materia_id`, `nome` and `codigo`) and a `GRUPOS` dictionary with 3 groups pointing to those subjects. This will be the starting point for the API's data.
3. If you version the project with Git, make a commit: `git commit -m "Create the sample data in Python"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You have `grupos = {1: {...}, 2: {...}}` and need to return the group with identifier `grupo_id`, but it may not exist. Why is `grupos.get(grupo_id)` safer than `grupos[grupo_id]`?

Answer: because `grupos[grupo_id]` stops the program with a `KeyError` when the key does not exist, and the program crashes. `grupos.get(grupo_id)`, on the other hand, returns `None`, and the code can test `if grupo is None:` and respond with a 404 in a controlled way. In an API, a request for a nonexistent group is a normal situation, not a program error.

## // Module summary

- [ ] I can write functions with parameters, default values and `return`.
- [ ] I can create and use lists, slices and list comprehensions.
- [ ] I can create and use dictionaries, and I know the difference between `[]` and `.get()`.
- [ ] I know what type hints are, and that they do not validate on their own.
- [ ] I can catch an exception with `try` and `except`.
- [ ] I have an initial `dados.py` with subjects and groups.

---

**Next module:** `07-your-first-api-with-fastapi.md`: the language is ready. Time to install FastAPI and make your first API respond.

`Study Material // Coffee & Code`
