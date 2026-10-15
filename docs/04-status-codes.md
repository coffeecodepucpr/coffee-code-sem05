# Módulo 04, Status Codes

`SEM 05 // API RESTful Central`

---

## // Antes de começar

O método diz o que o cliente quer fazer. O **código de status** diz o que aconteceu. Este módulo apresenta os códigos que uma API de CRUD usa, quando devolver cada um, e por que escolher o código certo importa tanto quanto devolver os dados certos.

## // O problema: como o cliente sabe se deu certo?

Imagine uma API que responde sempre com o mesmo código, e que informa o resultado apenas dentro do corpo: `{"erro": "grupo não encontrado"}` ou `{"ok": true}`. Cada cliente teria que abrir o corpo e adivinhar o formato para saber se algo falhou. Os códigos de status resolvem isso: antes mesmo de ler o corpo, o cliente já sabe a categoria do resultado, e qualquer programa entende o mesmo código.

## // As cinco famílias

> **STATUS CODE: EM PALAVRAS SIMPLES**
> É um número de três dígitos, na primeira linha da resposta, que resume o resultado do pedido. O **primeiro dígito** indica a família, e as famílias contam uma história.

<div align="center">
<img src="./assets/status-codes-familias.svg" alt="As famílias de status HTTP: 1xx informativo, 2xx sucesso, 3xx redirecionamento, 4xx erro do cliente, 5xx erro do servidor" width="640">
</div>

| Família | Significado | Em uma frase |
|---|---|---|
| **1xx** | Informativo | "Recebi, continue" (raro em uma API de CRUD) |
| **2xx** | Sucesso | "Deu certo" |
| **3xx** | Redirecionamento | "O que você procura está em outro endereço" |
| **4xx** | Erro do **cliente** | "O pedido tem um problema, e quem precisa corrigir é quem pediu" |
| **5xx** | Erro do **servidor** | "O pedido estava correto, mas eu falhei" |

A diferença entre 4xx e 5xx é a mais importante do módulo: ela diz **de quem é a culpa**. Um 404 pede que o cliente corrija o endereço. Um 500 diz que o cliente não tem o que fazer, e que o problema está no servidor.

## // Os códigos da API desta semana

| Código | Nome | Quando devolver | Exemplo real na API |
|---|---|---|---|
| **200** | OK | Deu certo, e há dados para devolver | `GET /grupos/3` devolve o grupo |
| **201** | Created | Um recurso novo foi criado | `POST /grupos` devolve o grupo criado |
| **204** | No Content | Deu certo, e não há nada para devolver | `DELETE /grupos/7` devolve só o status |
| **404** | Not Found | O recurso pedido não existe | `GET /grupos/99` |
| **405** | Method Not Allowed | A rota existe, mas não aceita esse método | `DELETE /grupos` |
| **409** | Conflict | O pedido entra em conflito com o estado atual | Criar um grupo com nome já usado na matéria |
| **422** | Unprocessable Content | O corpo ou os parâmetros têm formato ou valor inválido | Nome curto demais, ou `grupo_id` igual a `abc` |
| **500** | Internal Server Error | Algo deu errado dentro do servidor | Um erro de programação não tratado |

Outros códigos aparecem em APIs com login, como o `401` (não identificado) e o `403` (sem permissão). Eles ficam fora desta semana.

## // Cada código em ação

Todas as respostas abaixo foram obtidas da API desta semana, em execução.

**200 OK**, com os dados no corpo:

```
GET /grupos/3

HTTP/1.1 200 OK
{"nome_grupo":"Modelagem e SQL","materia_id":3,"max_participantes":8,"descricao":"Encontros online às terças e aos sábados","grupo_id":3,"criado_em":"2026-09-03T12:00:00Z"}
```

**201 Created**, com o endereço do novo recurso no cabeçalho `Location`:

```
POST /grupos

HTTP/1.1 201 Created
location: /grupos/7
{"nome_grupo":"Cálculo II na prática","materia_id":1,"max_participantes":5,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

**204 No Content**, sem corpo nenhum:

```
DELETE /grupos/7

HTTP/1.1 204 No Content
```

**404 Not Found**, com uma mensagem no campo `detail`:

```
GET /grupos/99

HTTP/1.1 404 Not Found
{"detail":"Grupo não encontrado"}
```

**405 Method Not Allowed**, com o cabeçalho `allow` listando um método aceito pela rota:

```
DELETE /grupos

HTTP/1.1 405 Method Not Allowed
allow: GET
{"detail":"Method Not Allowed"}
```

**409 Conflict**, ao repetir um `POST` que cria um grupo igual a outro:

```
POST /grupos

HTTP/1.1 409 Conflict
{"detail":"Já existe um grupo com esse nome nessa matéria"}
```

**422**, quando o valor enviado é inválido. O FastAPI explica exatamente onde está o problema (`loc`) e qual é ele (`msg`):

```
POST /grupos  com nome_grupo igual a "ab"

HTTP/1.1 422 Unprocessable Entity
{"detail":[{"type":"string_too_short","loc":["body","nome_grupo"],"msg":"String should have at least 3 characters","input":"ab","ctx":{"min_length":3}}]}
```

**500**, quando o próprio código da API quebra. Aqui, uma rota com uma divisão por zero:

```
HTTP/1.1 500 Internal Server Error
Internal Server Error
```

Repare que no 500 o servidor não explica nada ao cliente, e isso é proposital: detalhes internos de um erro não devem vazar para quem está de fora.

> **UM DETALHE SOBRE O 422**
> O nome oficial atual do código 422 é "Unprocessable Content". Servidores mais antigos, incluindo o `uvicorn` usado nesta semana, ainda escrevem "Unprocessable Entity" na linha de status. No FastAPI, a constante antiga `HTTP_422_UNPROCESSABLE_ENTITY` está **depreciada**: o Python avisa e pede para usar `HTTP_422_UNPROCESSABLE_CONTENT`. Muitos tutoriais da internet ainda usam o nome velho, então você vai encontrá-lo por aí.

## // Como escolher entre 404, 409 e 422

São os três códigos que mais geram dúvida, porque os três dizem "o pedido tem um problema". A diferença está no tipo de problema:

| Situação | Código | Por quê |
|---|---|---|
| O identificador na rota não existe (`/grupos/99`) | **404** | Falta o recurso que o endereço aponta |
| Um valor enviado tem formato ou regra inválida (nome curto, `materia_id` que não existe) | **422** | O pedido está mal formado ou quebra uma regra de validação |
| O pedido é válido, mas colide com o que já existe (nome repetido) | **409** | O formato está certo, mas o estado atual do servidor não permite |

Uma regra prática: **404 é sobre o endereço, 422 é sobre o conteúdo, 409 é sobre o estado.**

## // Bom exemplo × mau exemplo

**Mau exemplo**: sempre `200`, com o erro dentro do corpo:

```
GET /grupos/99

HTTP/1.1 200 OK
{"erro": true, "mensagem": "grupo não encontrado"}
```

Todo cliente precisa saber que, nessa API, `200` pode significar fracasso, e abrir o corpo para conferir. Ferramentas que dependem do código, como as de monitoramento, acham que está tudo bem.

**Bom exemplo**: o código conta a verdade:

```
GET /grupos/99

HTTP/1.1 404 Not Found
{"detail":"Grupo não encontrado"}
```

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Devolver `200` com mensagem de erro no corpo | É mais fácil que escolher um código | Use o código que descreve o resultado e deixe o corpo só para explicar |
| Devolver `500` para erro do cliente (por exemplo, um dado inválido) | Um erro não tratado no código vira 500 | Valide a entrada e devolva `422` ou `404`, e deixe o `500` para falhas reais |
| Devolver `200` ao criar um recurso | `200` parece o código "padrão" de sucesso | Use `201` e informe o endereço no `Location` |
| Devolver `204` com corpo | O `204` significa "sem conteúdo" | Se há dados para devolver, use `200` |
| Trocar `404` e `422` | Os dois dizem que "algo não foi encontrado ou está errado" | `404` para o endereço, `422` para o conteúdo |
| Usar o nome antigo da constante do 422 | Tutoriais antigos usam `HTTP_422_UNPROCESSABLE_ENTITY` | Use `HTTP_422_UNPROCESSABLE_CONTENT` |

## // Prática guiada

1. Anote, em uma folha, os oito códigos da tabela desta seção e, ao lado de cada um, uma frase com as suas palavras explicando quando usá-lo.
2. Releia a regra "404 é sobre o endereço, 422 é sobre o conteúdo, 409 é sobre o estado" e invente, para cada código, um exemplo diferente dos deste módulo, usando o recurso `/livros` de uma biblioteca.

## // Pratique sozinho

> **DESAFIO**
> Qual código você devolveria em cada situação do recurso `/grupos`? (a) Um grupo foi alterado com sucesso e a resposta traz o grupo atualizado. (b) A pessoa pede `GET /grupos/abc`. (c) A pessoa tenta apagar um grupo que não existe. (d) A pessoa cria um grupo com `max_participantes` igual a 500, e o limite é 50. (e) Um grupo foi apagado com sucesso. (f) A pessoa tenta criar um grupo com um nome que outro grupo da mesma matéria já usa. Confira com a tabela dos códigos.

## // Aplicando no projeto da semana

1. No `README.md`, acrescente a seção "Códigos de status por rota".
2. Para cada uma das oito rotas planejadas, escreva o código de sucesso e os códigos de erro que você espera (por exemplo: `GET /grupos/{grupo_id}`: sucesso `200`, erros `404` e `422`).
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Planeja os códigos de status de cada rota"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Uma API devolve `500 Internal Server Error` quando a pessoa envia um `materia_id` que não existe, porque o código tenta acessar um item inexistente e quebra. Qual é o problema, e que código seria o certo?

Resposta: o problema é que um erro **da pessoa** (um valor que não existe) está sendo tratado como erro **do servidor**. O cliente não consegue saber que a culpa foi do dado que ele enviou, e quem mantém a API recebe alertas de falha que não são falhas. O código certo é o `422`, devolvido por uma verificação explícita antes de usar o valor, deixando o `500` apenas para falhas reais do servidor.

## // Resumo do módulo

- [ ] Sei as cinco famílias de status e a diferença entre 4xx e 5xx.
- [ ] Sei os oito códigos usados na API desta semana e quando devolver cada um.
- [ ] Sei diferenciar 404 (endereço), 422 (conteúdo) e 409 (estado).
- [ ] Sei por que não se devolve `200` com erro no corpo.
- [ ] Sei que a constante antiga do 422 está depreciada no FastAPI.

---

**Próximo módulo:** `05-python-ambiente-tipos-e-decisoes.md`, a teoria de HTTP está pronta. Hora de preparar o ambiente e aprender a linguagem em que a API será escrita.

`Material de Estudo // Coffee & Code`
