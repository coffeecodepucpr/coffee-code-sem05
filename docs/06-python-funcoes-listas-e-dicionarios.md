# Módulo 06, Python: Funções, Listas e Dicionários

Português · [English](../docs-eng/06-python-functions-lists-and-dictionaries.md)

`SEM 05 // API RESTful Central`

---

## // Antes de começar

No Módulo 05 você preparou o ambiente e viu os blocos básicos do Python. Este módulo apresenta as quatro ferramentas que a API usa o tempo todo: funções, listas, dicionários e dicas de tipo. Quando você abrir o código da API, quase tudo o que aparecer vai ser uma combinação delas.

## // O problema: lógica repetida e dados soltos

Um programa que repete o mesmo trecho cinco vezes fica difícil de manter, e um programa com dados espalhados em dezenas de variáveis fica difícil de entender. As funções resolvem o primeiro problema, e as listas e dicionários resolvem o segundo.

## // Funções

> **FUNÇÃO: EM PALAVRAS SIMPLES**
> É um bloco de código com um nome, que recebe valores de entrada (os **parâmetros**), faz um trabalho e pode devolver um resultado com `return`. Escreve-se uma vez e usa-se quantas vezes for preciso.

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

Três pontos importantes:

- `def` define a função, e o corpo é indentado, como em um `if`.
- `vagas=10` é um **valor padrão**: se a chamada não informar `vagas`, vale 10.
- Os argumentos podem ser passados **pelo nome** (`vagas=4`), em qualquer ordem. O FastAPI usa muito esse estilo.

## // Listas

> **LISTA: EM PALAVRAS SIMPLES**
> É uma sequência ordenada de valores, escrita entre colchetes. Cada valor tem uma posição, e a contagem das posições começa em **zero**.

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

| Operação | Resultado |
|---|---|
| `materias[0]` | O primeiro item |
| `materias[-1]` | O último item |
| `materias[1:3]` | Uma fatia: da posição 1 até a 2 (a 3 não entra) |
| `materias.append(x)` | Acrescenta um item no fim |
| `len(materias)` | A quantidade de itens |

A segunda linha do exemplo usa uma **compreensão de lista**: `[m for m in materias if len(m) > 10]` lê-se "uma lista com cada `m` das matérias, só se o tamanho de `m` for maior que 10". É a forma curta e muito comum de filtrar uma lista, e a API a usa para filtrar grupos.

## // Dicionários

> **DICIONÁRIO: EM PALAVRAS SIMPLES**
> É uma coleção de pares **chave: valor**, escrita entre chaves. Em vez de buscar por posição, você busca pela chave. É a estrutura que mais se parece com um objeto JSON.

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

| Operação | Resultado |
|---|---|
| `grupo["nome_grupo"]` | O valor da chave. Se a chave não existe, dá erro (`KeyError`) |
| `grupo.get("max")` | O valor da chave, ou `None` se ela não existe |
| `grupo.get("max", 10)` | O valor da chave, ou `10` se ela não existe |
| `"grupo_id" in grupo` | `True` se a chave existe |
| `grupo["nova"] = valor` | Cria ou troca uma chave |

### > Dicionários de dicionários: o formato dos dados da API

A API guarda os grupos em um dicionário cuja chave é o identificador e cujo valor é outro dicionário com os dados do grupo:

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

Buscar um grupo por identificador é só `grupos.get(2)`. Se ele não existir, o resultado é `None`, e a API usa isso para decidir se devolve um 404. O `del` remove uma chave.

## // Contador automático: next

Para dar um identificador novo a cada grupo criado, a API usa um **contador** da biblioteca padrão do Python:

```python
import itertools
contador = itertools.count(7)
print(next(contador), next(contador), next(contador))
```

```
7 8 9
```

Cada chamada a `next(contador)` devolve o número seguinte. A linha `import itertools` traz para o programa uma biblioteca que já vem com o Python.

## // Dicas de tipo

```python
def buscar(grupos, grupo_id: int) -> dict | None:
    return grupos.get(grupo_id)

print(buscar(grupos, 2), buscar(grupos, 99))
```

```
{'nome': 'B'} None
```

Os trechos `: int` e `-> dict | None` são **dicas de tipo**. Elas dizem que `grupo_id` deve ser um inteiro e que a função devolve um dicionário ou `None`. O símbolo `|` significa "ou".

> **AS DICAS DE TIPO NÃO VALIDAM NADA SOZINHAS**
> O Python **não confere** as dicas de tipo ao rodar. Uma função declarada com `x: int` aceita `"texto"` sem reclamar. O que o FastAPI faz é **ler** essas dicas e transformá-las em validação automática dos dados que chegam à API. Esse é o grande segredo do framework, e o Módulo 08 mostra isso em ação.

## // Erros e exceções

Quando algo dá errado, o Python interrompe o programa e mostra uma **exceção**. Dá para capturá-la e reagir:

```python
try:
    int("abc")
except ValueError as erro:
    print("erro:", erro)
```

```
erro: invalid literal for int() with base 10: 'abc'
```

O FastAPI tem um jeito próprio de transformar exceções em respostas HTTP, que o Módulo 10 apresenta.

> **SE VOCÊ JÁ PROGRAMA EM OUTRA LINGUAGEM (OPCIONAL)**
> Se você conhece JavaScript, o dicionário do Python corresponde ao objeto literal, e a lista corresponde ao *array*. A compreensão de lista faz o papel do `.filter()` e do `.map()`, e o `try`/`except` corresponde ao `try`/`catch`. Se você não conhece JavaScript, ignore este quadro.

## // Bom exemplo × mau exemplo

**Mau exemplo**: esquecer o `return`:

```python
def dobro(x):
    x * 2

print(dobro(4))
```

```
None
```

A conta é feita, mas o resultado é jogado fora. Uma função sem `return` devolve `None`.

**Bom exemplo**: devolver o resultado:

```python
def dobro(x):
    return x * 2

print(dobro(4))
```

```
8
```

## // Erros comuns

| Erro | O que diz | Por que acontece | Como corrigir |
|---|---|---|---|
| `KeyError` | `KeyError: 'max'` | Acessar com `grupo["max"]` uma chave que não existe | Use `grupo.get("max")` quando a chave pode faltar |
| `IndexError` | `list index out of range` | Pedir uma posição que a lista não tem | Confira o tamanho com `len(lista)` |
| `TypeError` | `somar() missing 1 required positional argument: 'b'` | Chamar uma função com menos argumentos do que ela exige | Passe todos os argumentos, ou defina valores padrão |
| Função devolve `None` | (nenhuma mensagem) | Faltou o `return` | Acrescente o `return` |
| Achar que `x: int` valida | (nenhuma mensagem) | As dicas de tipo não são conferidas pelo Python | Lembre que a validação vem do FastAPI e do Pydantic |

## // Prática guiada

1. Escreva uma função `status_do_grupo(participantes, vagas)` que devolva `"cheio"`, `"quase cheio"` ou `"com vagas"`.
2. Crie um dicionário `grupo` com as chaves `nome_grupo`, `materia_id` e `max_participantes`, e escreva cada par com um `for` e `.items()`.
3. Crie uma lista com cinco nomes de grupos e use uma compreensão de lista para guardar só os que têm mais de 15 caracteres.
4. Crie um dicionário de dicionários com três grupos, remova um com `del` e confira o resultado com `.get()`.

## // Pratique sozinho

> **DESAFIO**
> Crie um dicionário `grupos` com três grupos, em que a chave é o identificador. Escreva uma função `buscar_grupo(grupos, grupo_id)` que devolva o grupo, ou `None` se ele não existir. Depois escreva uma função `listar_por_materia(grupos, materia_id)` que devolva uma **lista** só com os grupos daquela matéria, usando uma compreensão de lista.

## // Aplicando no projeto da semana

1. Dentro da pasta `api-grupos`, crie o arquivo `dados.py`.
2. Escreva nele um dicionário `MATERIAS` com 3 matérias (chaves `materia_id`, `nome` e `codigo`) e um dicionário `GRUPOS` com 3 grupos que apontem para essas matérias. Este será o ponto de partida dos dados da API.
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Cria os dados de exemplo em Python"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você tem `grupos = {1: {...}, 2: {...}}` e precisa devolver o grupo de identificador `grupo_id`, mas ele pode não existir. Por que `grupos.get(grupo_id)` é mais seguro do que `grupos[grupo_id]`?

Resposta: porque `grupos[grupo_id]` interrompe o programa com um `KeyError` quando a chave não existe, e o programa cai. Já `grupos.get(grupo_id)` devolve `None`, e o código pode testar `if grupo is None:` e responder com um 404 de forma controlada. Em uma API, um pedido por um grupo inexistente é uma situação normal, e não um erro do programa.

## // Resumo do módulo

- [ ] Sei escrever funções com parâmetros, valores padrão e `return`.
- [ ] Sei criar e usar listas, fatias e compreensões de lista.
- [ ] Sei criar e usar dicionários, e a diferença entre `[]` e `.get()`.
- [ ] Sei o que são dicas de tipo, e que elas não validam sozinhas.
- [ ] Sei capturar uma exceção com `try` e `except`.
- [ ] Tenho um `dados.py` inicial com matérias e grupos.

---

**Próximo módulo:** `07-sua-primeira-api-com-fastapi.md`: a linguagem está pronta. Hora de instalar o FastAPI e fazer a primeira API responder.

`Material de Estudo // Coffee & Code`
