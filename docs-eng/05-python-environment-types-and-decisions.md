# Module 05, Python: Environment, Types and Decisions

[Português](../docs/05-python-ambiente-tipos-e-decisoes.md) · English

`WEEK 05 // Central RESTful API`

---

## // Before you start

This week's API will be written in Python. This module does two jobs: setting up your computer to run Python in an organized way, and introducing the first pieces of the language. Module 06 completes what is missing (functions, lists and dictionaries). No programming experience is needed.

## // The problem: without an environment, nothing runs; without the language, nothing reads

A Python program needs an installed interpreter, a way to install libraries without messing up the rest of the computer, and for you to know how to read what is written. These are three different concerns, and this module handles each one in order.

## // What Python is

> **PYTHON: IN SIMPLE WORDS**
> It is a programming language known for reading cleanly, almost like English text. Instead of braces or closing words, it uses **indentation** (the spaces at the start of the line) to show what belongs to each block.

## // Installing Python

FastAPI requires **Python 3.10 or higher**. This week's examples were run on Python 3.12. Download the installer from `python.org`. On Windows, the installer usually offers an option to add Python to the `PATH` (the exact button names may vary): check it.

Check the installation by opening a terminal:

| System | Command |
|---|---|
| Windows | `py --version` |
| macOS and Linux | `python3 --version` |

```
Python 3.12.3
```

If the version is lower than 3.10, install a newer one before continuing.

## // The terminal, in one minute

The terminal is a window where you type commands instead of clicking. Three commands are enough for now:

| Command | What it does |
|---|---|
| `cd folder-name` | Enters a folder |
| `cd ..` | Goes back one folder |
| `mkdir folder-name` | Creates a folder |

Create the project folder and go into it:

```
mkdir api-grupos
cd api-grupos
```

## // The virtual environment

> **VIRTUAL ENVIRONMENT: IN SIMPLE WORDS**
> It is the project's own folder, with a copy of Python and a separate space for the libraries it uses. This keeps one project's libraries from interfering with another's, and keeps different versions from clashing.

Create and activate the environment, **inside the** `api-grupos` **folder**:

| Step | macOS and Linux | Windows |
|---|---|---|
| Create | `python3 -m venv .venv` | `py -m venv .venv` |
| Activate | `source .venv/bin/activate` | `.venv\Scripts\activate` |

When the environment is active, the terminal shows `(.venv)` at the start of the line. To leave it, use `deactivate`.

> **ABOUT WINDOWS AND POWERSHELL**
> Creating the environment was tested on Linux. The Windows activation commands follow the official Python documentation and **were not tested by the author**. In PowerShell, the activation script is called `.venv\Scripts\Activate.ps1` and, depending on the computer's security settings, it may be blocked. If that happens, use the Command Prompt (`cmd`) to activate the environment.

With the environment active, `python --version` shows the environment's version, and `pip --version` shows the library installer Module 07 will use. From here on, **whenever you open a new terminal to work on the project, activate the environment first**.

## // Running your first program

A Python program is a text file with the `.py` extension. Create the file `tipos.py` in the project folder, with this content:

```python
nome = "Cálculo I"
codigo = "MAT101"
vagas = 6
ativo = True
descricao = None

print(type(nome), type(vagas), type(ativo), type(descricao))
print(f"{nome} ({codigo}) tem {vagas} vagas")
```

Run it with `python tipos.py`. The result:

```
<class 'str'> <class 'int'> <class 'bool'> <class 'NoneType'>
Cálculo I (MAT101) tem 6 vagas
```

> The examples keep Portuguese names (`nome` = name, `vagas` = spots, `ativo` = active, `descricao` = description) to match the project's code.

## // Variables and types

In Python, a variable is born the moment it receives a value, with no special word before it. The basic types:

| Type | What it holds | Example |
|---|---|---|
| `str` | Text, in single or double quotes | `"Cálculo I"` |
| `int` | Whole number | `6` |
| `float` | Decimal number, with a dot | `3.5` |
| `bool` | True or false (capitalized) | `True`, `False` |
| `None` | Absence of a value | `None` |

The `f"..."` in the example is an **f-string**: text in which whatever is in braces is replaced by the variable's value. It is the most practical way to build messages.

## // Operators

```python
print(7 // 2, 7 % 2, 7 / 2, 2 ** 3)
print("cálculo" in nome.lower(), nome.upper(), len(nome))
```

```
3 1 3.5 8
True CÁLCULO I 9
```

| Operator | Meaning |
|---|---|
| `//` | Integer division (`7 // 2` gives `3`) |
| `%` | Remainder of the division (`7 % 2` gives `1`) |
| `/` | Regular division (`7 / 2` gives `3.5`) |
| `**` | Power |
| `==`, `!=` | Equal, not equal |
| `and`, `or`, `not` | And, or, not |
| `in` | Is contained in |

## // Decisions: if, elif and else

```python
participantes = 4
if participantes >= vagas:
    print("Grupo cheio")
elif participantes >= vagas - 1:
    print("Quase cheio")
else:
    print("Vagas disponíveis")
```

```
Vagas disponíveis
```

Three details that make a difference in Python: the condition ends with a **colon**, the block that belongs to it is **indented** (use 4 spaces), and `elif` is short for "else, if".

## // Loops: for and while

```python
for i in range(1, 4):
    print("encontro", i)

tentativas = 0
while tentativas < 3:
    tentativas += 1
print("tentativas:", tentativas)
```

```
encontro 1
encontro 2
encontro 3
tentativas: 3
```

`range(1, 4)` generates the numbers from 1 to 3 (the upper limit is **not** included). `for` goes through a sequence, and `while` repeats while the condition is true.

## // What counts as true

Inside an `if`, Python accepts any value, and decides whether it "counts as true":

```python
print(bool(0), bool(""), bool(None), bool([]), bool("0"), bool([0]))
```

```
False False False False True True
```

These count as **false**: `0`, empty text, `None` and empty lists. Everything else counts as true, including the text `"0"` and a list that contains a zero. This lets you write `if descricao:` to ask "is there a description?".

> **IF YOU ALREADY CODE IN ANOTHER LANGUAGE (OPTIONAL)**
> If you know JavaScript, the comparison helps: `let x = 5` becomes `x = 5`; `true`, `false` and `null` become `True`, `False` and `None`; `===` becomes `==`; `&&`, `||` and `!` become `and`, `or` and `not`; `else if` becomes `elif`; the braces `{ }` become a colon plus indentation; and the backtick *template literal* becomes the f-string. If you do not know JavaScript, ignore this box: nothing that follows depends on it.

## // Good example × bad example

**Bad example**: a single equals sign in the condition:

```python
vagas = 6
if vagas = 6:
    print("cheio")
```

```
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

A single `=` **assigns** a value. To **compare**, you need two: `==`.

**Good example**: comparing with `==`:

```python
vagas = 6
if vagas == 6:
    print("cheio")
```

## // Common mistakes

All the messages below were obtained by running the code.

| Mistake | What it says | Why it happens | How to fix it |
|---|---|---|---|
| `IndentationError` | `expected an indented block after 'if' statement on line 2` | The block after an `if` is not indented | Indent the block with 4 spaces |
| `IndentationError` | `unindent does not match any outer indentation level` | A line has a different indentation from its siblings | Always use 4 spaces, and never mix spaces with tabs |
| `NameError` | `name 'nmoe' is not defined` | A typo in a variable name | Check the spelling |
| `TypeError` | `can only concatenate str (not "int") to str` | Trying to add text and a number with `+` | Use an f-string: `f"Vagas: {vagas}"` |
| `SyntaxError` | `Maybe you meant '==' ...` | A `=` instead of `==` in a condition | Use `==` to compare |
| The `pip` command installs outside the project | (no error message) | The virtual environment was not active | Activate the environment and check for `(.venv)` in the terminal |
| `python: command not found` | (varies by system) | On macOS and Linux, the command is usually `python3`; on Windows, `py` | Use the command shown in the installation table |

## // Guided practice

1. Create the `api-grupos` folder, the virtual environment, and activate it.
2. Create the `tipos.py` file and run it. Then change the value of `vagas` and run it again.
3. Add a decision with `if`, `elif` and `else` that writes "Group full", "Almost full" or "Spots available".
4. Add a `for` with `range` that writes the numbers from 1 to 5.
5. Deliberately cause the `NameError` and `IndentationError` errors, and read the messages.

## // Practice on your own

> **CHALLENGE**
> Write a program with the variables `nome_grupo`, `vagas` and `participantes`. It should write, with an f-string, a sentence like "Modelagem e SQL: 6 of 8 spots taken", and right after that say how many spots are left. If none are left, it should write "Group full".

## // Applying it to the week's project

1. Confirm the virtual environment exists in the `api-grupos` folder and that, when activated, `python --version` shows 3.10 or higher.
2. If you version the project with Git, create a `.gitignore` file with the line `.venv/` and make a commit: `git commit -m "Set up the project environment"`. The virtual environment should not go into the repository.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Why create a virtual environment for each project, instead of installing everything directly into the computer's Python?

Answer: because each project may need different versions of the same libraries. Installing everything in the same place, installing the version one project needs can break another. In a virtual environment, each project has its own space, and removing the project means deleting a folder, without leaving traces on the rest of the computer.

## // Module summary

- [ ] I have Python 3.10 or higher installed and I know how to check the version.
- [ ] I can create and activate a virtual environment.
- [ ] I can run a `.py` file from the terminal.
- [ ] I know the basic types, f-strings and operators.
- [ ] I can write decisions (`if`, `elif`, `else`) and loops (`for`, `while`), respecting the indentation.
- [ ] I know which values Python treats as false.

---

**Next module:** `06-python-functions-lists-and-dictionaries.md`: with the environment ready and the basics of the language, what is left is organizing logic into functions and storing data in lists and dictionaries.

`Study Material // Coffee & Code`
