# Módulo 05, Python: Ambiente, Tipos e Decisões

Português · [English](../docs-eng/05-python-environment-types-and-decisions.md)

`SEM 05 // API RESTful Central`

---

## // Antes de começar

A API desta semana será escrita em Python. Este módulo cumpre duas tarefas: preparar o seu computador para rodar Python de forma organizada, e apresentar os primeiros pedaços da linguagem. O Módulo 06 completa o que falta (funções, listas e dicionários). Nenhuma experiência com programação é necessária.

## // O problema: sem ambiente, nada roda; sem linguagem, nada se lê

Um programa em Python precisa de um interpretador instalado, de um jeito de instalar bibliotecas sem bagunçar o resto do computador, e de você saber ler o que está escrito. São três preocupações diferentes, e este módulo trata de cada uma na ordem.

## // O que é Python

> **PYTHON: EM PALAVRAS SIMPLES**
> É uma linguagem de programação conhecida por ter uma leitura limpa, quase como texto em inglês. Em vez de chaves ou palavras de fechamento, ela usa a **indentação** (os espaços no começo da linha) para mostrar o que pertence a cada bloco.

## // Instalando o Python

O FastAPI exige **Python 3.10 ou superior**. Os exemplos desta semana foram executados no Python 3.12. Baixe o instalador em `python.org`. No Windows, o instalador costuma oferecer uma opção para adicionar o Python ao `PATH` (os nomes exatos dos botões podem variar): marque-a.

Confira a instalação abrindo um terminal:

| Sistema | Comando |
|---|---|
| Windows | `py --version` |
| macOS e Linux | `python3 --version` |

```
Python 3.12.3
```

Se a versão for menor que 3.10, instale uma mais nova antes de continuar.

## // O terminal, em um minuto

O terminal é uma janela onde você digita comandos em vez de clicar. Três comandos bastam por enquanto:

| Comando | O que faz |
|---|---|
| `cd nome-da-pasta` | Entra em uma pasta |
| `cd ..` | Volta uma pasta |
| `mkdir nome-da-pasta` | Cria uma pasta |

Crie a pasta do projeto e entre nela:

```
mkdir api-grupos
cd api-grupos
```

## // O ambiente virtual

> **AMBIENTE VIRTUAL: EM PALAVRAS SIMPLES**
> É uma pasta própria do projeto, com uma cópia do Python e um espaço separado para as bibliotecas que ele usa. Isso evita que bibliotecas de um projeto interfiram em outro, e que versões diferentes briguem entre si.

Crie e ative o ambiente, **dentro da pasta** `api-grupos`:

| Passo | macOS e Linux | Windows |
|---|---|---|
| Criar | `python3 -m venv .venv` | `py -m venv .venv` |
| Ativar | `source .venv/bin/activate` | `.venv\Scripts\activate` |

Quando o ambiente está ativo, o terminal mostra `(.venv)` no começo da linha. Para sair dele, use `deactivate`.

> **SOBRE O WINDOWS E O POWERSHELL**
> A criação do ambiente foi testada em Linux. Os comandos de ativação do Windows seguem a documentação oficial do Python e **não foram testados pelo autor**. No PowerShell, o script de ativação se chama `.venv\Scripts\Activate.ps1` e, dependendo da configuração de segurança do computador, pode ser bloqueado. Se isso acontecer, use o Prompt de Comando (`cmd`) para ativar o ambiente.

Com o ambiente ativo, `python --version` mostra a versão do ambiente, e `pip --version` mostra o instalador de bibliotecas que o Módulo 07 vai usar. Daqui em diante, **sempre que abrir um terminal novo para trabalhar no projeto, ative o ambiente primeiro**.

## // Rodando o primeiro programa

Um programa em Python é um arquivo de texto com a extensão `.py`. Crie o arquivo `tipos.py` na pasta do projeto, com este conteúdo:

```python
nome = "Cálculo I"
codigo = "MAT101"
vagas = 6
ativo = True
descricao = None

print(type(nome), type(vagas), type(ativo), type(descricao))
print(f"{nome} ({codigo}) tem {vagas} vagas")
```

Rode com `python tipos.py`. O resultado:

```
<class 'str'> <class 'int'> <class 'bool'> <class 'NoneType'>
Cálculo I (MAT101) tem 6 vagas
```

## // Variáveis e tipos

Em Python, uma variável nasce no momento em que recebe um valor, sem nenhuma palavra especial antes. Os tipos básicos:

| Tipo | O que guarda | Exemplo |
|---|---|---|
| `str` | Texto, entre aspas simples ou duplas | `"Cálculo I"` |
| `int` | Número inteiro | `6` |
| `float` | Número decimal, com ponto | `3.5` |
| `bool` | Verdadeiro ou falso (com inicial maiúscula) | `True`, `False` |
| `None` | Ausência de valor | `None` |

O `f"..."` do exemplo é uma **f-string**: um texto em que o que está entre chaves é substituído pelo valor da variável. É o jeito mais prático de montar mensagens.

## // Operadores

```python
print(7 // 2, 7 % 2, 7 / 2, 2 ** 3)
print("cálculo" in nome.lower(), nome.upper(), len(nome))
```

```
3 1 3.5 8
True CÁLCULO I 9
```

| Operador | Significado |
|---|---|
| `//` | Divisão inteira (`7 // 2` dá `3`) |
| `%` | Resto da divisão (`7 % 2` dá `1`) |
| `/` | Divisão comum (`7 / 2` dá `3.5`) |
| `**` | Potência |
| `==`, `!=` | Igual, diferente |
| `and`, `or`, `not` | E, ou, não |
| `in` | Está contido em |

## // Decisões: if, elif e else

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

Três detalhes que fazem a diferença em Python: a condição termina com **dois pontos**, o bloco que pertence a ela é **indentado** (use 4 espaços), e `elif` é a abreviação de "senão, se".

## // Repetições: for e while

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

`range(1, 4)` gera os números de 1 até 3 (o limite superior **não** entra). O `for` percorre uma sequência, e o `while` repete enquanto a condição for verdadeira.

## // O que conta como verdadeiro

Dentro de um `if`, o Python aceita qualquer valor, e decide se ele "vale como verdadeiro":

```python
print(bool(0), bool(""), bool(None), bool([]), bool("0"), bool([0]))
```

```
False False False False True True
```

Valem como **falso**: `0`, texto vazio, `None` e listas vazias. Todo o resto vale como verdadeiro, incluindo o texto `"0"` e uma lista que contém um zero. Isso permite escrever `if descricao:` para perguntar "existe uma descrição?".

> **SE VOCÊ JÁ PROGRAMA EM OUTRA LINGUAGEM (OPCIONAL)**
> Se você conhece JavaScript, a comparação ajuda: `let x = 5` vira `x = 5`; `true`, `false` e `null` viram `True`, `False` e `None`; `===` vira `==`; `&&`, `||` e `!` viram `and`, `or` e `not`; `else if` vira `elif`; as chaves `{ }` viram dois pontos mais indentação; e o *template literal* com crases vira a f-string. Se você não conhece JavaScript, ignore este quadro: nada do que vem depois depende dele.

## // Bom exemplo × mau exemplo

**Mau exemplo**: um sinal de igual na condição:

```python
vagas = 6
if vagas = 6:
    print("cheio")
```

```
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Um `=` **atribui** um valor. Para **comparar**, são dois: `==`.

**Bom exemplo**: comparar com `==`:

```python
vagas = 6
if vagas == 6:
    print("cheio")
```

## // Erros comuns

Todas as mensagens abaixo foram obtidas ao executar o código.

| Erro | O que diz | Por que acontece | Como corrigir |
|---|---|---|---|
| `IndentationError` | `expected an indented block after 'if' statement on line 2` | O bloco depois de um `if` não está indentado | Indente o bloco com 4 espaços |
| `IndentationError` | `unindent does not match any outer indentation level` | Uma linha tem indentação diferente das irmãs | Use sempre 4 espaços, e nunca misture espaços com tabulação |
| `NameError` | `name 'nmoe' is not defined` | Erro de digitação no nome de uma variável | Confira a grafia |
| `TypeError` | `can only concatenate str (not "int") to str` | Tentar somar um texto com um número usando `+` | Use uma f-string: `f"Vagas: {vagas}"` |
| `SyntaxError` | `Maybe you meant '==' ...` | Um `=` no lugar de `==` em uma condição | Use `==` para comparar |
| Comando `pip` instala fora do projeto | (sem mensagem de erro) | O ambiente virtual não estava ativo | Ative o ambiente e confira o `(.venv)` no terminal |
| `python: command not found` | (varia por sistema) | No macOS e no Linux, o comando costuma ser `python3`; no Windows, `py` | Use o comando indicado na tabela de instalação |

## // Prática guiada

1. Crie a pasta `api-grupos`, o ambiente virtual e ative-o.
2. Crie o arquivo `tipos.py` e rode-o. Depois, troque o valor de `vagas` e rode de novo.
3. Acrescente uma decisão com `if`, `elif` e `else` que escreva "Grupo cheio", "Quase cheio" ou "Vagas disponíveis".
4. Acrescente um `for` com `range` que escreva os números de 1 a 5.
5. Provoque de propósito os erros `NameError` e `IndentationError`, e leia as mensagens.

## // Pratique sozinho

> **DESAFIO**
> Escreva um programa com as variáveis `nome_grupo`, `vagas` e `participantes`. Ele deve escrever, com uma f-string, uma frase como "Modelagem e SQL: 6 de 8 vagas ocupadas", e logo depois informar quantas vagas restam. Se não restar nenhuma, deve escrever "Grupo cheio".

## // Aplicando no projeto da semana

1. Confirme que o ambiente virtual existe na pasta `api-grupos` e que, ativado, `python --version` mostra 3.10 ou superior.
2. Se você versiona o projeto com Git, crie o arquivo `.gitignore` com a linha `.venv/` e faça um commit: `git commit -m "Prepara o ambiente do projeto"`. O ambiente virtual não deve ir para o repositório.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Por que se cria um ambiente virtual para cada projeto, em vez de instalar tudo diretamente no Python do computador?

Resposta: porque cada projeto pode precisar de versões diferentes das mesmas bibliotecas. Instalando tudo no mesmo lugar, instalar a versão que um projeto exige pode quebrar outro. No ambiente virtual, cada projeto tem o seu espaço, e remover o projeto é apagar uma pasta, sem deixar rastros no resto do computador.

## // Resumo do módulo

- [ ] Tenho o Python 3.10 ou superior instalado e sei conferir a versão.
- [ ] Sei criar e ativar um ambiente virtual.
- [ ] Sei rodar um arquivo `.py` pelo terminal.
- [ ] Sei os tipos básicos, as f-strings e os operadores.
- [ ] Sei escrever decisões (`if`, `elif`, `else`) e repetições (`for`, `while`), respeitando a indentação.
- [ ] Sei quais valores o Python trata como falsos.

---

**Próximo módulo:** `06-python-funcoes-listas-e-dicionarios.md`: com o ambiente pronto e a base da linguagem, falta organizar a lógica em funções e guardar dados em listas e dicionários.

`Material de Estudo // Coffee & Code`
