# Módulo 10, CRUD: Lendo Dados

`SEM 05 // API RESTful Central`

---

## // Antes de começar

Com os modelos prontos, você começa a construir a API de verdade. O CRUD tem quatro letras, e o **R** de *Read* (ler) é a mais simples e a mais usada, então é por ela que se começa. Neste módulo você implementa as rotas que listam e buscam, incluindo a resposta de **"não encontrado"**.

## // O problema: de onde vêm os dados, e o que fazer quando não existem

Uma rota de leitura precisa de duas coisas: um lugar onde os dados estejam, e uma decisão sobre o que responder quando o pedido aponta para algo que não existe. Esta semana os dados vivem em memória, em dicionários do Python, e a decisão de "não existe" é um `404`.

## // Os dados do projeto

Crie o arquivo `dados.py` na pasta `api-grupos`. Ele guarda as matérias e os grupos de exemplo (aqui, o começo do arquivo; o conteúdo completo está em `example/api-basica/dados.py`):

```python
import itertools
from datetime import datetime, timezone

MATERIAS = {
    1: {"materia_id": 1, "nome": "Cálculo I", "codigo": "MAT101"},
    2: {"materia_id": 2, "nome": "Estrutura de Dados", "codigo": "INF201"},
    # ... mais quatro matérias
}


def _data(dia: int) -> datetime:
    return datetime(2026, 9, dia, 12, 0, tzinfo=timezone.utc)


GRUPOS = {
    1: {"grupo_id": 1, "nome_grupo": "Cálculo passo a passo", "materia_id": 1,
        "max_participantes": 6, "descricao": None, "criado_em": _data(1)},
    # ... mais cinco grupos
}

CONTADOR_GRUPOS = itertools.count(7)
```

O formato é o do Módulo 06: um dicionário de dicionários, com o identificador como chave. O `CONTADOR_GRUPOS` vai gerar os identificadores dos grupos que forem criados (7, 8, 9, ...).

## // Preparando o main.py

O `main.py` final começa assim:

```python
from fastapi import FastAPI, HTTPException, Response, status

import dados
from schemas import GrupoCreate, GrupoOut, GrupoPatch, GrupoUpdate, MateriaOut

app = FastAPI(title="API Central: Buscador de Grupos de Estudo", version="1.0.0")
```

Duas coisas novas: o `import dados`, que traz o arquivo de dados como módulo (assim, `dados.GRUPOS` é o dicionário de grupos), e o `status`, uma coleção de nomes legíveis para os códigos (`status.HTTP_404_NOT_FOUND` vale 404).

## // Listar uma coleção

```python
@app.get("/materias", response_model=list[MateriaOut])
def listar_materias():
    return list(dados.MATERIAS.values())
```

`dados.MATERIAS.values()` devolve os dicionários de cada matéria, e `list(...)` os transforma em uma lista. O `response_model=list[MateriaOut]` diz que a resposta é uma **lista** de matérias, cada uma com o formato do modelo.

```
GET /materias

200  [{"materia_id":1,"nome":"Cálculo I","codigo":"MAT101"}, ...]   (6 itens)
```

## // Buscar um item e o 404

```python
@app.get("/materias/{materia_id}", response_model=MateriaOut)
def buscar_materia(materia_id: int):
    materia = dados.MATERIAS.get(materia_id)
    if materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matéria não encontrada")
    return materia
```

O raciocínio é o do Módulo 06: `.get()` devolve `None` se a chave não existe, e a função decide o que fazer. O novo ingrediente é o `HTTPException`:

> **HTTPEXCEPTION: EM PALAVRAS SIMPLES**
> É uma exceção especial do FastAPI. Quando você a **levanta** com `raise`, a função para ali, e o FastAPI transforma a exceção em uma resposta HTTP com o código e a mensagem que você escolheu.

```
GET /materias/1
200  {"materia_id":1,"nome":"Cálculo I","codigo":"MAT101"}

GET /materias/99
404  {"detail":"Matéria não encontrada"}
```

O `raise` interrompe a função, e por isso **não é preciso** um `else`: o `return materia` só é alcançado quando a matéria existe.

## // Reutilizando o 404: a função de apoio

A busca de um grupo vai ser usada em quatro rotas (buscar, substituir, alterar e apagar). Em vez de repetir o `if` quatro vezes, ele vira uma função:

```python
def buscar_grupo_ou_404(grupo_id: int) -> dict:
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
    return grupo


@app.get("/grupos/{grupo_id}", response_model=GrupoOut)
def buscar_grupo(grupo_id: int):
    return buscar_grupo_ou_404(grupo_id)
```

```
GET /grupos/3
200  {"nome_grupo":"Modelagem e SQL","materia_id":3,"max_participantes":8,"descricao":"Encontros online às terças e aos sábados","grupo_id":3,"criado_em":"2026-09-03T12:00:00Z"}

GET /grupos/99
404  {"detail":"Grupo não encontrado"}
```

O `HTTPException` levantado **dentro** da função de apoio também interrompe a rota que a chamou. Por isso a rota `buscar_grupo` é uma linha só.

## // Listar com filtros

A rota que lista os grupos aceita dois parâmetros de consulta opcionais, o termo de busca `q` e a matéria `materia_id`:

```python
@app.get("/grupos", response_model=list[GrupoOut])
def listar_grupos(q: str | None = None, materia_id: int | None = None):
    grupos = list(dados.GRUPOS.values())
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g["nome_grupo"].lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g["materia_id"] == materia_id]
    return grupos
```

A lógica é a do Módulo 06: começa-se com todos os grupos, e cada filtro **reduz** a lista com uma compreensão de lista. O `.lower()` nos dois lados faz a busca ignorar maiúsculas e minúsculas.

```
GET /grupos?q=prática
200  [{"nome_grupo":"Estruturas na prática","materia_id":2, ... }]

GET /grupos?materia_id=1
200  [{"nome_grupo":"Cálculo passo a passo","materia_id":1, ... }]

GET /grupos?q=zzz
200  []
```

> **BUSCA SEM RESULTADO NÃO É UM 404**
> Repare no último exemplo: `GET /grupos?q=zzz` devolve **200** com uma lista **vazia**. O `404` é para quando o **endereço** aponta para algo que não existe (`/grupos/99`). Uma coleção que existe, mas não tem nenhum item que atenda ao filtro, é uma resposta válida: a lista só está vazia.

## // Testando pelo Swagger

Abra o `/docs`. Os parâmetros `q` e `materia_id` aparecem como campos de texto opcionais na rota `GET /grupos`, e o campo `grupo_id` aparece como obrigatório em `GET /grupos/{grupo_id}`. Teste:

1. `GET /grupos` sem preencher nada.
2. `GET /grupos` com `q` igual a `prática`.
3. `GET /grupos/3`, e depois `GET /grupos/99`.
4. `GET /grupos/abc` e leia o `422`.

## // Bom exemplo × mau exemplo

**Mau exemplo**: devolver `200` com uma mensagem quando o item não existe:

```python
@app.get("/grupos/{grupo_id}")
def buscar_grupo(grupo_id: int):
    grupo = dados.GRUPOS.get(grupo_id)
    if grupo is None:
        return {"mensagem": "grupo não encontrado"}
    return grupo
```

O cliente recebe `200 OK` e precisa abrir o corpo para descobrir que na verdade falhou.

**Bom exemplo**: o código conta a verdade:

```python
if grupo is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo não encontrado")
```

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `KeyError` e um `500` ao buscar um id inexistente | Usou `dados.GRUPOS[grupo_id]` em vez de `.get()` | Use `.get()` e trate o `None` com `HTTPException` |
| `return HTTPException(...)` não devolve 404 | Faltou o `raise`: o objeto foi só devolvido como dado | Use `raise HTTPException(...)` |
| A busca devolve `404` quando nada casa | Confundir "coleção vazia" com "recurso inexistente" | Devolva `200` com `[]` |
| A rota devolve um dicionário sem os campos do modelo | O `response_model` espera campos que o dicionário não tem | Confira que os dados têm todos os campos do modelo |
| Uma alteração na lista de resultados muda os dados originais | Alterar um dicionário que veio de `dados.GRUPOS` | Leia sem modificar nas rotas de leitura |
| Mensagem de erro em inglês misturada com português | Mensagens padrão (`Not Found`) convivem com as suas | Defina o `detail` de cada `HTTPException` no idioma do projeto |

## // Prática guiada

1. Crie o `dados.py` e o `schemas.py` na pasta `api-grupos` (use os arquivos de `example/api-basica` como referência).
2. No `main.py`, escreva as rotas `GET /materias` e `GET /materias/{materia_id}`.
3. Escreva a função `buscar_grupo_ou_404` e as rotas `GET /grupos` e `GET /grupos/{grupo_id}`.
4. Teste cada uma pelo Swagger, incluindo um identificador que não existe e um filtro sem resultados.

## // Pratique sozinho

> **DESAFIO**
> Acrescente à rota `GET /grupos` um terceiro filtro, `min_vagas`, que mantenha só os grupos com `max_participantes` maior ou igual ao valor informado. Teste `min_vagas=6` e `min_vagas=100`, e confirme que o segundo devolve `200` com lista vazia, e não um erro.

## // Aplicando no projeto da semana

1. Deixe as rotas de leitura funcionando no `main.py` da pasta `api-grupos`.
2. Percorra, pelo Swagger, os cinco casos de teste da seção anterior e anote, no `README.md`, o código que cada um devolveu.
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Implementa as rotas de leitura"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Qual é a diferença entre `GET /grupos/99` e `GET /grupos?materia_id=99`, em termos do código de status devolvido?

Resposta: `GET /grupos/99` aponta para **um item específico** que não existe, então devolve `404`. Já `GET /grupos?materia_id=99` pede a **coleção** de grupos filtrada por uma matéria. A coleção existe, e o filtro apenas não encontra nenhum item, então a resposta é `200` com `[]`. O endereço diz quem você procura, e o filtro diz quais itens da coleção você quer ver.

## // Resumo do módulo

- [ ] Sei guardar dados em dicionários e importar o módulo `dados`.
- [ ] Sei escrever uma rota que lista uma coleção, com `response_model=list[...]`.
- [ ] Sei buscar um item e responder `404` com `HTTPException`.
- [ ] Sei reutilizar o `404` em uma função de apoio.
- [ ] Sei implementar filtros opcionais com parâmetros de consulta.
- [ ] Sei que uma busca sem resultado devolve `200` com lista vazia.

---

**Próximo módulo:** `11-crud-criar-atualizar-e-apagar.md`, a leitura está pronta. Falta o resto do CRUD: criar, atualizar e apagar.

`Material de Estudo // Coffee & Code`
