# Módulo 12, Swagger na Prática

`SEM 05 // API RESTful Central`

---

## // Antes de começar

A API já funciona, e o Swagger apareceu de graça desde o Módulo 07. Este módulo faz duas coisas: ensina a usar o Swagger como a sua principal **ferramenta de teste**, e ensina a escrever uma documentação que alguém de fora entenda sem perguntar nada.

## // O problema: API sem documentação é adivinhação

Quem for usar a sua API precisa saber quais rotas existem, o que enviar em cada uma, o que volta e quais erros esperar. Sem isso, a pessoa chuta, erra, e acaba lendo o seu código. A documentação resolve, e o FastAPI a gera a partir do próprio código, então ela só fica desatualizada se o código também ficar.

## // OpenAPI e Swagger: dois nomes, duas coisas

> **OPENAPI: EM PALAVRAS SIMPLES**
> É uma especificação, ou seja, um formato padronizado de texto (JSON) para descrever uma API: as rotas, os parâmetros, os corpos aceitos e as respostas possíveis.

> **SWAGGER UI: EM PALAVRAS SIMPLES**
> É uma ferramenta que lê uma descrição no formato OpenAPI e desenha uma página interativa, onde cada rota pode ser testada. É a página do `/docs`.

O fluxo é: o FastAPI **lê o seu código** e monta o OpenAPI em `/openapi.json`; o Swagger UI **lê o OpenAPI** e desenha o `/docs`. A página alternativa `/redoc` lê o mesmo arquivo.

## // O OpenAPI por dentro

Abra `http://127.0.0.1:8000/openapi.json`. O arquivo tem cinco blocos principais:

| Bloco | O que contém |
|---|---|
| `openapi` | A versão da especificação (nesta API, `3.1.0`) |
| `info` | O título, a descrição e a versão da API |
| `paths` | Cada rota, e dentro dela cada método com os parâmetros e as respostas |
| `components` | Os modelos reutilizados (os "schemas") |
| `tags` | A descrição dos grupos de rotas |

Esta API tem quatro caminhos (`/materias`, `/materias/{materia_id}`, `/grupos` e `/grupos/{grupo_id}`) e sete modelos, entre eles `GrupoCreate`, `GrupoOut`, `GrupoPatch`, `GrupoUpdate` e `MateriaOut`. Este é o trecho real da rota `GET /materias/{materia_id}`:

```json
{
  "tags": ["materias"],
  "summary": "Busca uma matéria pelo identificador",
  "operationId": "buscar_materia_materias__materia_id__get",
  "parameters": [
    {
      "name": "materia_id",
      "in": "path",
      "required": true,
      "schema": {"type": "integer", "title": "Materia Id"}
    }
  ],
  "responses": {
    "200": {"description": "Successful Response", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MateriaOut"}}}},
    "404": {"description": "Matéria não encontrada"},
    "422": {"description": "Validation Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}}}
  }
}
```

(O arquivo real vem com a formatação mais compacta; aqui ele foi organizado para leitura.) Compare com o código da rota: o `materia_id: int` virou `"type": "integer"`, o `response_model=MateriaOut` virou a referência na resposta `200`, e o `responses={404: ...}` virou a entrada `404`. O `422` entrou sozinho, porque toda rota com parâmetros pode falhar na validação.

## // Anatomia da página /docs

<div align="center">
<img src="./assets/swagger-esquematico.svg" alt="Esquema da página do Swagger UI, com cabeçalho, grupos de rotas, uma rota expandida e a lista de modelos" width="640">
</div>

O esquema é uma simplificação, e a sua tela pode ter pequenas diferenças. A estrutura é esta:

- **No alto:** o título, a versão e a descrição que você escreveu no `FastAPI(...)`.
- **Os grupos (tags):** as rotas aparecem agrupadas pelo nome da `tag`.
- **Cada rota:** uma linha com o método (cada um com a sua cor), o caminho e o resumo.
- **Uma rota expandida:** os parâmetros, o corpo da requisição (com um exemplo editável), o botão **Try it out** e as respostas possíveis.
- **No fim:** a seção **Schemas**, com todos os modelos.

## // Usando o Swagger como ferramenta de teste

Esta é a rotina para testar qualquer rota. A interface do Swagger está em inglês.

1. **Expanda** a rota clicando nela.
2. Clique em **Try it out**. Os campos ficam editáveis.
3. Preencha os parâmetros, e, se houver, edite o **corpo** (a área de texto já vem com o exemplo).
4. Clique em **Execute**.
5. Leia o resultado em **Server response**: o **código**, o **corpo** (*Response body*) e os **cabeçalhos** (*Response headers*).
6. Compare com a seção **Responses**, logo abaixo, que lista o que a rota **promete** devolver.

O Swagger mostra também o comando `curl` equivalente ao que você acabou de executar. Ele é um ótimo jeito de aprender a sintaxe do `curl` sem digitar.

Para o `POST /grupos`, o corpo vem preenchido com o exemplo que está no modelo `GrupoCreate`, graças a este trecho do código:

```python
model_config = ConfigDict(
    json_schema_extra={
        "examples": [
            {
                "nome_grupo": "Cálculo II na prática",
                "materia_id": 1,
                "max_participantes": 5,
                "descricao": "Listas de exercícios às quartas",
            }
        ]
    }
)
```

## // Documentando no código

O que aparece no Swagger vem de quatro lugares do código:

| Onde você escreve | Aparece no Swagger como | Exemplo |
|---|---|---|
| `FastAPI(title=..., description=..., version=...)` | O cabeçalho da página. A descrição aceita **Markdown** | `title="API Central: Buscador de Grupos de Estudo"` |
| `openapi_tags=[{"name": ..., "description": ...}]` | A descrição de cada grupo de rotas | `{"name": "grupos", "description": "CRUD completo dos grupos de estudo."}` |
| `summary="..."` no decorador | O texto ao lado de cada rota | `summary="Cria um grupo"` |
| `responses={404: {"description": "..."}}` | A lista de respostas possíveis | `responses={404: {"description": "Grupo não encontrado"}}` |
| `Field(description="...")` no modelo | A explicação de cada campo | `Field(description="Nome do grupo de estudo")` |

E o que o FastAPI preenche **sozinho** quando você não escreve nada:

```python
@app.get("/grupos")
def listar_grupos():
    """Devolve todos os grupos cadastrados."""
    return []
```

| Campo | Valor gerado |
|---|---|
| `summary` | `Listar Grupos` (o nome da função, com maiúsculas e espaços) |
| `description` | `Devolve todos os grupos cadastrados.` (a **docstring** da função) |
| `operationId` | `listar_grupos_grupos_get` |

Por isso nomear bem as funções já documenta metade da API. Uma função chamada `f1` vira, no Swagger, uma rota de resumo `F1`, que não ajuda ninguém.

## // Documentação pública também revela a sua API

Quem abre o `/docs` vê todas as rotas e todos os campos, e o `/openapi.json` entrega a mesma informação em formato de máquina. Para esconder a documentação:

```python
app = FastAPI(docs_url=None, redoc_url=None)
```

> **DESLIGAR O /DOCS NÃO ESCONDE O OPENAPI**
> No teste desta semana, uma aplicação criada com `docs_url=None` e `redoc_url=None` passou a responder **404** em `/docs` e em `/redoc`, mas o `/openapi.json` **continuou respondendo 200**. Para desligar tudo, é preciso também `openapi_url=None`. Esta semana a API roda só no seu computador, então deixe a documentação ligada: ela é a sua melhor ferramenta de estudo.

## // Bom exemplo × mau exemplo

**Mau exemplo**: rotas sem resumo, descrição nem respostas documentadas:

```python
@app.post("/grupos", status_code=201)
def f(g: GrupoCreate): ...
```

No Swagger aparece uma rota "F", sem nenhuma indicação de que ela pode devolver `409` ou `422`.

**Bom exemplo**: documentação que antecipa as dúvidas:

```python
@app.post(
    "/grupos",
    status_code=201,
    summary="Cria um grupo",
    responses={
        409: {"description": "Já existe um grupo com esse nome nessa matéria"},
        422: {"description": "Dados inválidos, ou matéria inexistente"},
    },
)
def criar_grupo(novo: GrupoCreate): ...
```

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| A página `/docs` abre em branco | Sem internet para carregar os arquivos do Swagger | Conecte-se e recarregue |
| O Swagger mostra o `422` mas não o `404` | O `404` é levantado no código, e o FastAPI não adivinha | Declare `responses={404: {...}}` |
| O corpo do exemplo vem com valores sem sentido (`"string"`, `0`) | Não foi definido um exemplo no modelo | Use `json_schema_extra` com `examples` |
| O Swagger não reflete uma mudança | O servidor não recarregou, ou a página está em cache | Confira o terminal e recarregue a página |
| O teste pelo Swagger funciona, mas o `curl` dá `422` | O `curl` esqueceu o `Content-Type` | Copie o `curl` que o próprio Swagger gera |
| Documentar uma resposta que a rota não devolve | O código mudou e a documentação ficou parada | Revise o `responses` sempre que mudar as regras |

## // Prática guiada

1. Abra o `/openapi.json` e localize: `info`, os quatro caminhos e o modelo `GrupoCreate`.
2. No `/docs`, percorra todas as rotas e execute cada uma com **Try it out**.
3. No `POST /grupos`, edite o corpo para provocar um `409` e um `422`, e compare a resposta com a seção **Responses**.
4. Copie o comando `curl` que o Swagger mostra para uma rota e rode-o no terminal.
5. Troque o `summary` de uma rota e confira a mudança no `/docs` depois de salvar.

## // Pratique sozinho

> **DESAFIO**
> Escolha três rotas da sua API sem `summary` ou sem `responses` completos, e documente-as. Para cada uma, acrescente o `summary` e todas as respostas de erro que ela pode devolver (use a tabela de códigos do Módulo 11). Confira no `/docs` se cada resposta apareceu na lista.

## // Aplicando no projeto da semana

1. Garanta que o `FastAPI(...)` do `main.py` tenha `title`, `description` e `version`, e que as tags estejam descritas em `openapi_tags`.
2. Garanta que todas as rotas tenham `summary` e que as que podem falhar tenham `responses`.
3. Salve no `README.md` um trecho do `/openapi.json` (por exemplo, a rota `GET /grupos/{grupo_id}`) e explique, em uma linha, como o código gerou cada parte.
4. Se você versiona o projeto com Git, faça um commit: `git commit -m "Documenta a API para o Swagger"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você alterou a mensagem de erro de um `404` no código, mas esqueceu de atualizar o `responses={404: {"description": "..."}}` do decorador. O que o Swagger mostra, e o que a API devolve de fato?

Resposta: o Swagger mostra a descrição **antiga**, porque ela vem do `responses` escrito à mão, e não da mensagem que a função levanta. A API devolve a mensagem **nova**. É um dos poucos pontos em que a documentação pode ficar desatualizada, e por isso o `responses` descreve o **tipo** de resposta ("Grupo não encontrado"), e não um texto que mude a todo momento.

## // Resumo do módulo

- [ ] Sei a diferença entre OpenAPI (a descrição) e Swagger UI (a página).
- [ ] Sei os cinco blocos do `/openapi.json` e como o código vira cada parte.
- [ ] Sei testar qualquer rota pelo Swagger: **Try it out**, **Execute** e **Server response**.
- [ ] Sei documentar com `title`, `description`, `tags`, `summary`, `responses` e `Field`.
- [ ] Sei o que o FastAPI preenche sozinho (resumo e docstring).
- [ ] Sei que desligar o `/docs` não desliga o `/openapi.json`.

---

**Próximo módulo:** `13-projeto-guiado.md`, todas as peças estão prontas. Hora de montar a API completa do início ao fim.

`Material de Estudo // Coffee & Code`
