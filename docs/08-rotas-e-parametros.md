# Módulo 08, Rotas e Parâmetros

`SEM 05 // API RESTful Central`

---

## // Antes de começar

No Módulo 07 você escreveu rotas que não recebem nada. Uma API de verdade precisa receber valores: qual grupo? qual termo de busca? Este módulo mostra as duas formas de enviar valores pela URL, os parâmetros de **caminho** e de **consulta**, e uma das maiores vantagens do FastAPI: a validação automática desses valores.

## // O problema: cada pedido é diferente

A rota `/grupos/3` e a rota `/grupos/5` pedem coisas diferentes, mas seria absurdo escrever uma função para cada identificador. O que se quer é **uma** função que receba o número como entrada. É para isso que servem os parâmetros.

## // Parâmetros de caminho

> **PARÂMETRO DE CAMINHO: EM PALAVRAS SIMPLES**
> É uma parte variável da própria rota, marcada com chaves no decorador. O valor que o cliente escreve naquele ponto da URL chega à função como argumento.

```python
@app.get("/saudacao/{nome}")
def saudar(nome: str):
    return {"mensagem": f"Olá, {nome}!"}
```

```
GET /saudacao/Ana

{"mensagem":"Olá, Ana!"}
```

O nome entre chaves no decorador (`{nome}`) precisa ser **igual** ao nome do parâmetro da função (`nome`). É assim que o FastAPI sabe ligar um ao outro.

## // O tipo do parâmetro valida o valor

Veja o mesmo mecanismo com um número inteiro:

```python
@app.get("/vagas/{total}")
def vagas(total: int, ocupadas: int = 0):
    return {"total": total, "ocupadas": ocupadas, "livres": total - ocupadas}
```

Dois pedidos diferentes:

```
GET /vagas/6
200  {"total":6,"ocupadas":0,"livres":6}

GET /vagas/abc
422  {"detail":[{"type":"int_parsing","loc":["path","total"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

Você **não escreveu nenhuma validação**. A dica `total: int` foi suficiente: o FastAPI tentou converter `abc` para inteiro, falhou, e devolveu um `422` explicando o problema. Repare no campo `loc`: ele diz **onde** está o erro (`path`, ou seja, no caminho) e **qual** parâmetro (`total`).

É isso que o Módulo 06 prometeu: o Python não confere as dicas de tipo, mas o FastAPI as lê e as transforma em validação.

## // Parâmetros de consulta

> **PARÂMETRO DE CONSULTA: EM PALAVRAS SIMPLES**
> É um valor opcional enviado depois do `?` na URL, no formato `nome=valor`, com vários separados por `&`. Qualquer parâmetro da função que **não** está na rota vira um parâmetro de consulta.

No exemplo anterior, `ocupadas` não aparece na rota, então é um parâmetro de consulta:

```
GET /vagas/6?ocupadas=2
200  {"total":6,"ocupadas":2,"livres":4}

GET /vagas/6?ocupadas=x
422  {"detail":[{"type":"int_parsing","loc":["query","ocupadas"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"x"}]}
```

Agora o `loc` diz `query`. A regra de ouro sobre quando usar cada tipo:

| Tipo | Para quê | Exemplo |
|---|---|---|
| **Caminho** | Identificar **qual** recurso | `/grupos/3` |
| **Consulta** | Filtrar, buscar, ordenar ou paginar | `/grupos?q=sql&materia_id=3` |

### > Obrigatório ou opcional

| Declaração | Significado |
|---|---|
| `ocupadas: int` | **Obrigatório**: o pedido sem ele devolve 422 |
| `ocupadas: int = 0` | **Opcional**, com valor padrão `0` |
| `q: str \| None = None` | **Opcional**, e vale `None` quando não é enviado |

## // Validando melhor com Query

Para impor regras ao valor (tamanho mínimo, máximo), use `Query`:

```python
from typing import Annotated
from fastapi import Query

@app.get("/buscar")
def buscar(q: Annotated[str | None, Query(min_length=2, max_length=30)] = None, limite: int = 10):
    return {"q": q, "limite": limite}
```

```
GET /buscar
200  {"q":null,"limite":10}

GET /buscar?q=sql&limite=5
200  {"q":"sql","limite":5}

GET /buscar?q=s
422  {"detail":[{"type":"string_too_short","loc":["query","q"],"msg":"String should have at least 2 characters","input":"s","ctx":{"min_length":2}}]}
```

O `Annotated[...]` é o jeito atual de anexar regras a um tipo: lê-se "um texto ou `None`, com tamanho entre 2 e 30".

## // A ordem das rotas importa

Quando duas rotas podem casar com o mesmo endereço, o FastAPI usa **a primeira que foi declarada**:

```python
@app.get("/grupos/{grupo_id}")
def grupo_por_id(grupo_id: int):
    return {"grupo_id": grupo_id}

@app.get("/grupos/novo")
def tela_novo():
    return {"nunca": "chega aqui"}
```

```
GET /grupos/novo
422  {"detail":[{"type":"int_parsing","loc":["path","grupo_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"novo"}]}
```

A palavra `novo` casou com `{grupo_id}` antes de chegar à rota fixa, e a conversão para inteiro falhou. A solução é declarar as rotas **fixas** antes das rotas com parâmetro.

## // Bom exemplo × mau exemplo

**Mau exemplo**: validar à mão o que o tipo já valida:

```python
@app.get("/vagas/{total}")
def vagas(total):
    if not total.isdigit():
        return {"erro": "total precisa ser número"}
    ...
```

Esse código devolve `200` com a mensagem de erro (um problema que o Módulo 04 descreveu), repete um trabalho que o FastAPI já faz, e ainda rejeita valores como `-3`, que o tipo `int` aceitaria.

**Bom exemplo**: deixar o tipo trabalhar:

```python
@app.get("/vagas/{total}")
def vagas(total: int, ocupadas: int = 0):
    return {"total": total, "ocupadas": ocupadas, "livres": total - ocupadas}
```

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `422` ao chamar uma rota "certa" | O valor não casa com o tipo declarado (`abc` onde se espera `int`) | Leia o campo `loc` e o `msg`: eles dizem qual parâmetro e qual problema |
| O parâmetro da função não recebe o valor | O nome na rota (`{grupo_id}`) é diferente do nome na função | Use exatamente o mesmo nome nos dois lugares |
| Um parâmetro de consulta é tratado como obrigatório | Ele foi declarado sem valor padrão | Dê um padrão (`= 0`, `= None`) para torná-lo opcional |
| Uma rota fixa nunca é alcançada | Uma rota com parâmetro foi declarada antes | Declare as rotas fixas primeiro |
| O caractere `&` quebra a URL no terminal | O `&` tem significado especial em alguns terminais | Coloque a URL entre aspas |
| Acentos viram `%c3%a1` na URL | A URL só aceita certos caracteres, e codifica os demais | É normal: o servidor decodifica de volta sozinho |

## // Prática guiada

1. No `main.py`, acrescente a rota `/saudacao/{nome}` e teste pelo navegador e pelo Swagger.
2. Acrescente a rota `/vagas/{total}` com o parâmetro opcional `ocupadas`. Teste com e sem ele, e com valores inválidos.
3. Acrescente a rota `/buscar` com `q` validado por `Query`. Teste `q` com 1 caractere.
4. Declare `/grupos/{grupo_id}` antes de `/grupos/novo`, teste os dois endereços, e depois inverta a ordem e teste de novo.
5. No `/docs`, veja como os parâmetros aparecem nos formulários de cada rota.

## // Pratique sozinho

> **DESAFIO**
> Escreva a rota `GET /desconto/{preco}` que receba um preço (número decimal, `float`) e um parâmetro de consulta opcional `percentual` (inteiro, com padrão 10 e valor entre 0 e 100, usando `Query` com `ge` e `le`). A rota deve devolver o preço, o percentual e o preço final. Teste valores inválidos para os dois parâmetros e leia o `loc` de cada erro.

## // Aplicando no projeto da semana

1. Mantenha no `main.py` as rotas de exemplo deste módulo (elas serão removidas no Módulo 13, quando a API final for montada).
2. Anote, no `README.md`, qual parâmetro da API final vai ser de **caminho** e quais vão ser de **consulta**: o identificador do grupo, o termo de busca e o filtro por matéria.
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Adiciona rotas com parâmetros"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Na rota `GET /grupos/{grupo_id}`, a pessoa chama `/grupos/-5`. O tipo `int` aceita números negativos, então a validação passa. O que a sua função deve fazer, e que código a pessoa deve receber?

Resposta: a validação de tipo só garante que `-5` é um inteiro. Cabe à **sua função** procurar um grupo com esse identificador, não encontrar nenhum, e devolver `404 Not Found`. Na API desta semana, `GET /grupos/-5` e `GET /grupos/0` devolvem exatamente isso: `404` com `{"detail":"Grupo não encontrado"}`.

## // Resumo do módulo

- [ ] Sei declarar um parâmetro de caminho e ligá-lo ao argumento da função.
- [ ] Sei que o tipo do parâmetro valida o valor sem código extra.
- [ ] Sei declarar parâmetros de consulta, obrigatórios e opcionais.
- [ ] Sei quando usar parâmetro de caminho e quando usar de consulta.
- [ ] Sei usar `Query` para impor tamanho mínimo e máximo.
- [ ] Sei que rotas fixas devem vir antes de rotas com parâmetro.
- [ ] Sei ler o campo `loc` de um erro 422.

---

**Próximo módulo:** `09-modelos-com-pydantic.md`, os parâmetros de URL servem para valores simples. Para receber um grupo inteiro, em JSON, entram os modelos.

`Material de Estudo // Coffee & Code`
