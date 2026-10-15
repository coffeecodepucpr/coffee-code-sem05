# Módulo 18, Filtros, Ordenação e Paginação

`SEM 05 // API RESTful Central`

---

## // Antes de começar

> **TRILHA VETERANO, MÓDULO BÔNUS**
> Este módulo faz parte da trilha veterano e é um **bônus**: ele não é necessário para o entregável da semana. Quem segue a trilha principal pode pular para o `entregavel.md`.

Com seis grupos, devolver a lista inteira é inofensivo. Com seis mil, é um desperdício: o servidor monta uma resposta enorme, a rede a transporta, e quem a recebe só precisa dos primeiros itens. Este módulo ensina a devolver listas **em pedaços**, em uma ordem escolhida pelo cliente, usando as **dependências** do FastAPI. O código está em `example/api-limpa/`.

## // O problema: a lista inteira, sempre

Uma rota `GET /grupos` que devolve tudo tem três problemas conforme os dados crescem: a resposta demora, ocupa memória no servidor e no cliente, e obriga a tela a mostrar (ou descartar) milhares de itens. A solução padrão é a **paginação**.

## // Paginação com limit e offset

> **PAGINAÇÃO: EM PALAVRAS SIMPLES**
> É dividir uma lista grande em páginas. O cliente pede uma página por vez com dois parâmetros: `limit` (quantos itens quer) e `offset` (quantos itens pular antes de começar).

| Pedido | Significado |
|---|---|
| `?limit=2` | Os 2 primeiros itens |
| `?limit=2&offset=2` | Pule 2 e traga 2: a segunda página |
| `?limit=2&offset=4` | Pule 4 e traga 2: a terceira página |

A página `n` de tamanho `limit` começa em `offset = (n - 1) × limit`. Exemplo real, com a lista de seis grupos ordenada pelo nome:

```
GET /grupos?limit=2             ->  Cálculo passo a passo, Estruturas na prática
GET /grupos?limit=2&offset=2    ->  Modelagem e SQL, Processos e memória
GET /grupos?limit=2&offset=4    ->  Redes na unha, Requisitos e histórias
GET /grupos?limit=2&offset=10   ->  (lista vazia, e continua sendo 200)
```

Pedir uma página além do fim não é um erro: é só uma lista vazia.

## // Dependências com Depends

> **DEPENDÊNCIA: EM PALAVRAS SIMPLES**
> É uma função que o FastAPI executa **antes** da sua rota, entregando o resultado como argumento. Serve para reaproveitar uma lógica (como ler `limit` e `offset`) em várias rotas, sem copiar o código.

Você já usou uma dependência no Módulo 15: o `ServicoGruposDep` entrega o serviço às rotas. As de paginação e ordenação ficam no mesmo arquivo, `app/api/dependencias.py`:

```python
def paginacao(
    limit: Annotated[int, Query(ge=1, le=100, description="Quantos itens devolver")] = 10,
    offset: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
) -> dict:
    return {"limit": limit, "offset": offset}


Paginacao = Annotated[dict, Depends(paginacao)]
```

E a rota recebe o resultado como um parâmetro comum:

```python
@router.get("", response_model=list[GrupoOut], summary="Lista os grupos")
def listar_grupos(response: Response, servico: ServicoGruposDep, paginacao: Paginacao, ordenacao: Ordenacao, q: str | None = None, materia_id: int | None = None):
    ...
```

Os parâmetros `limit` e `offset` **não aparecem** na assinatura da rota: o FastAPI os lê dentro da dependência, valida e entrega o dicionário pronto. Mas, no `/docs`, eles aparecem como parâmetros de consulta da rota, porque o OpenAPI reúne os de todas as dependências.

### > Os limites protegem a API

Veja o que o `Query(ge=1, le=100)` e o `Query(ge=0)` fazem na prática, com as respostas reais no formato único de erro do Módulo 16:

```
GET /grupos?limit=0     ->  422  query.limit   Input should be greater than or equal to 1
GET /grupos?limit=101   ->  422  query.limit   Input should be less than or equal to 100
GET /grupos?offset=-1   ->  422  query.offset  Input should be greater than or equal to 0
```

O teto de 100 itens (`le=100`) evita que alguém peça `limit=1000000` e sobrecarregue o servidor. **Toda API paginada precisa de um teto.**

## // Ordenação com valores permitidos

Para escolher o campo e o sentido da ordenação, usa-se o tipo `Literal`, que aceita **somente** os valores listados:

```python
def ordenacao(
    ordenar_por: Annotated[Literal["nome_grupo", "max_participantes", "criado_em"], Query(description="Campo de ordenação")] = "nome_grupo",
    ordem: Annotated[Literal["asc", "desc"], Query(description="Sentido da ordenação")] = "asc",
) -> dict:
    return {"ordenar_por": ordenar_por, "ordem": ordem}
```

Um valor fora da lista é recusado com um `422` que lista as opções válidas:

```
GET /grupos?ordenar_por=banana

422  query.ordenar_por   Input should be 'nome_grupo', 'max_participantes' or 'criado_em'
```

No OpenAPI, o `Literal` vira uma lista de valores permitidos (`enum`), e o Swagger costuma oferecê-los como uma lista de opções para escolher, em vez de um campo de texto livre.

## // Onde fica a lógica: no serviço

Na arquitetura do Módulo 15, a rota **não** filtra, ordena nem corta a lista: ela só repassa os valores ao serviço, que cuida de tudo e devolve **a página e o total**:

```python
def listar(self, q=None, materia_id=None, ordenar_por="nome_grupo", ordem="asc", limit=10, offset=0) -> tuple[list[Grupo], int]:
    """Devolve a página pedida e o total de grupos que atendem aos filtros."""
    grupos = self._grupos.listar()
    if q is not None:
        grupos = [g for g in grupos if q.lower() in g.nome_grupo.lower()]
    if materia_id is not None:
        grupos = [g for g in grupos if g.materia_id == materia_id]
    chave = (lambda g: g.nome_grupo.lower()) if ordenar_por == "nome_grupo" else (lambda g: getattr(g, ordenar_por))
    grupos.sort(key=chave, reverse=ordem == "desc")
    return grupos[offset : offset + limit], len(grupos)
```

A função `lambda` é uma função pequena e sem nome: aqui, ela diz **por qual valor** comparar cada grupo. Para o nome, compara-se em minúsculas, para que `"Redes"` e `"cálculo"` fiquem em ordem alfabética de verdade. Repare no `return`: o total (`len(grupos)`) é calculado **antes** do corte (`grupos[offset : offset + limit]`).

## // O total de itens: o cabeçalho X-Total-Count

Quem recebe uma página precisa saber **quantas páginas existem**. Mas a resposta é uma lista, e uma lista não tem lugar para um número extra. A solução usada aqui é devolver o total em um **cabeçalho**:

```python
grupos, total = servico.listar(q=q, materia_id=materia_id, ordenar_por=..., ordem=..., limit=..., offset=...)
response.headers["X-Total-Count"] = str(total)
return grupos
```

Uma resposta real, com ordenação decrescente pelo limite de participantes:

```
GET /grupos?limit=2&ordenar_por=max_participantes&ordem=desc

HTTP/1.1 200 OK
x-total-count: 6
[Modelagem e SQL (limite 8), Cálculo passo a passo (limite 6)]
```

O total é calculado **depois do filtro e antes da paginação**: com `?q=prática&limit=1`, o total é 1 (só um grupo atende ao filtro), não 6. É o número que a tela precisa para desenhar "página 1 de N".

> **A ALTERNATIVA: UM ENVELOPE**
> Outra forma comum é devolver um objeto no lugar da lista, como `{"total": 6, "itens": [...]}`. Ela tem a vantagem de ficar visível no corpo, e a desvantagem de mudar o formato da resposta (quem esperava uma lista quebra). O cabeçalho mantém a lista como está, e por isso foi o escolhido aqui.

## // Bom exemplo × mau exemplo

**Mau exemplo**: paginar na tela, depois de receber tudo:

```
GET /grupos        ->  10.000 grupos, 4 MB de JSON
(a tela mostra só os 10 primeiros e joga o resto fora)
```

**Bom exemplo**: pedir só a página necessária:

```
GET /grupos?limit=10&offset=0   ->  10 grupos
```

Quem faz o trabalho no servidor economiza rede, memória e tempo de todos os clientes.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Uma página vazia devolve `404` | Confundir "página além do fim" com "recurso inexistente" | Devolva `200` com lista vazia |
| Pedir `limit=1000000` derruba o servidor | Faltou o teto no `limit` | Use `Query(ge=1, le=100)` |
| Confundir `offset` com número da página | Os dois parecem "onde começar" | `offset` conta **itens** pulados: a página `n` começa em `(n - 1) × limit` |
| Dois itens com o mesmo valor de ordenação trocam de lugar entre pedidos | Em muitos sistemas (bancos de dados, por exemplo) a ordem entre empates não é garantida. Nesta API em memória ela é estável, mas o hábito vale | Acrescente um segundo critério fixo, como o `grupo_id` |
| O total não bate com a página | O total foi calculado depois de cortar a lista | Calcule `len(grupos)` **antes** do corte |
| `422` ao pedir uma ordenação | O valor não está no `Literal` | Use um dos valores listados na mensagem de erro |

## // Prática guiada

1. Abra o `app/api/dependencias.py` e leia `paginacao` e `ordenacao`.
2. Rode a API e teste no Swagger: `limit=2` nas três páginas, `ordenar_por=max_participantes&ordem=desc`, e os valores inválidos.
3. Abra o `ServicoGrupos.listar` e confirme onde o total é calculado em relação ao corte.
4. Rode `pytest tests/test_listagem.py` e leia os cinco testes.

## // Pratique sozinho

> **DESAFIO**
> Acrescente `materia_id` à lista de valores permitidos do `ordenar_por` e implemente o desempate: quando dois grupos tiverem o mesmo valor no campo escolhido, o de menor `grupo_id` vem primeiro. Dica: a função `chave` pode devolver uma **tupla**, como `(getattr(g, campo), g.grupo_id)`. Escreva um teste que confirme a ordem.

## // Aplicando no projeto da semana

1. Se você seguiu a trilha veterano, mantenha a paginação e a ordenação na sua API em camadas.
2. No `README.md`, descreva os parâmetros `limit`, `offset`, `ordenar_por` e `ordem`, e o cabeçalho `X-Total-Count`.
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Adiciona filtros, ordenação e paginação"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> O `X-Total-Count` deve valer 6 em `GET /grupos?q=prática&limit=1`? Ou deve valer outro número?

Resposta: deve valer **1**, o número de grupos que atendem ao filtro `q=prática` (só `Estruturas na prática`). O total é calculado depois dos filtros e antes da paginação, porque ele serve para a tela saber quantas páginas existem **daquela busca**, e não do cadastro inteiro. O `limit=1` afeta só quantos itens vêm no corpo, e não o total.

## // Resumo do módulo

- [ ] Sei o que é paginação e como `limit` e `offset` funcionam.
- [ ] Sei criar uma dependência com `Depends` e reaproveitá-la em várias rotas.
- [ ] Sei validar `limit` e `offset` com `Query(ge=..., le=...)` e por que o teto importa.
- [ ] Sei restringir valores com `Literal` e ordenar com `sort`.
- [ ] Sei devolver o total de itens em um cabeçalho, e o que calcular antes do corte.
- [ ] Sei por que a lógica de listar fica no serviço, e não na rota.

---

**Próximo passo:** `entregavel.md`, a revisão final de tudo que a Semana 05 pediu.

`Material de Estudo // Coffee & Code`
