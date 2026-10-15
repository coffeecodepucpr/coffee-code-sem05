# Exemplos de requisições, Semana 05

Este arquivo reúne as requisições com `curl` usadas nos módulos, com as respostas **reais** de uma execução da API (`example/api-basica`, servidor ligado com `fastapi dev main.py`).

Execute **na ordem**: algumas dependem das anteriores (o grupo 7 é criado no `POST`, e só depois alterado e apagado). O cabeçalho `date` foi omitido, e o valor de `criado_em` muda a cada execução.

No Windows, `curl` pode ser um apelido de outro comando no PowerShell (use `curl.exe`), e as aspas do JSON podem exigir ajustes. Estes comandos foram executados em Linux e **não foram testados no Windows**. O Swagger (`/docs`) faz o mesmo sem nenhum desses problemas.

## Buscar um grupo (200)

```
curl -i http://127.0.0.1:8000/grupos/3
```

```
HTTP/1.1 200 OK
content-length: 175
content-type: application/json

{"nome_grupo":"Modelagem e SQL","materia_id":3,"max_participantes":8,"descricao":"Encontros online às terças e aos sábados","grupo_id":3,"criado_em":"2026-09-03T12:00:00Z"}
```

## Grupo que não existe (404)

```
curl -i http://127.0.0.1:8000/grupos/99
```

```
HTTP/1.1 404 Not Found
content-length: 34
content-type: application/json

{"detail":"Grupo não encontrado"}
```

## Buscar por nome (200)

```
curl "http://127.0.0.1:8000/grupos?q=pr%C3%A1tica"
```

```
[{"nome_grupo":"Estruturas na prática","materia_id":2,"max_participantes":5,"descricao":null,"grupo_id":2,"criado_em":"2026-09-02T12:00:00Z"}]
```

## Filtrar por matéria (200)

```
curl "http://127.0.0.1:8000/grupos?materia_id=1"
```

```
[{"nome_grupo":"Cálculo passo a passo","materia_id":1,"max_participantes":6,"descricao":null,"grupo_id":1,"criado_em":"2026-09-01T12:00:00Z"}]
```

## Identificador que não é número (422)

```
curl -i http://127.0.0.1:8000/grupos/abc
```

```
HTTP/1.1 422 Unprocessable Entity
content-length: 153
content-type: application/json

{"detail":[{"type":"int_parsing","loc":["path","grupo_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

## Criar um grupo (201)

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Cálculo II na prática", "materia_id": 1, "max_participantes": 5}'
```

```
HTTP/1.1 201 Created
content-length: 149
content-type: application/json
location: /grupos/7

{"nome_grupo":"Cálculo II na prática","materia_id":1,"max_participantes":5,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

## Criar o mesmo grupo de novo (409)

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Cálculo II na prática", "materia_id": 1}'
```

```
HTTP/1.1 409 Conflict
content-length: 61
content-type: application/json

{"detail":"Já existe um grupo com esse nome nessa matéria"}
```

## Matéria que não existe (422)

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Grupo fantasma", "materia_id": 99}'
```

```
HTTP/1.1 422 Unprocessable Entity
content-length: 38
content-type: application/json

{"detail":"A matéria 99 não existe"}
```

## Nome curto demais (422)

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "ab", "materia_id": 1}'
```

```
HTTP/1.1 422 Unprocessable Entity
content-length: 153
content-type: application/json

{"detail":[{"type":"string_too_short","loc":["body","nome_grupo"],"msg":"String should have at least 3 characters","input":"ab","ctx":{"min_length":3}}]}
```

## Esquecer o Content-Type (422)

```
curl -i -X POST http://127.0.0.1:8000/grupos \
  -d '{"nome_grupo": "Sem cabecalho", "materia_id": 1}'
```

```
HTTP/1.1 422 Unprocessable Entity
content-length: 198
content-type: application/json

{"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"Input should be a valid dictionary or object to extract fields from","input":"{\"nome_grupo\":\"Sem cabecalho\",\"materia_id\":1}"}]}
```

## Substituir um grupo (200)

```
curl -i -X PUT http://127.0.0.1:8000/grupos/7 \
  -H "Content-Type: application/json" \
  -d '{"nome_grupo": "Cálculo II revisado", "materia_id": 1, "max_participantes": 6}'
```

```
HTTP/1.1 200 OK
content-length: 146
content-type: application/json

{"nome_grupo":"Cálculo II revisado","materia_id":1,"max_participantes":6,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

## Alterar só um campo (200)

```
curl -i -X PATCH http://127.0.0.1:8000/grupos/7 \
  -H "Content-Type: application/json" \
  -d '{"max_participantes": 8}'
```

```
HTTP/1.1 200 OK
content-length: 146
content-type: application/json

{"nome_grupo":"Cálculo II revisado","materia_id":1,"max_participantes":8,"descricao":null,"grupo_id":7,"criado_em":"2026-10-08T12:52:39.463873Z"}
```

## Apagar um grupo (204)

```
curl -i -X DELETE http://127.0.0.1:8000/grupos/7
```

```
HTTP/1.1 204 No Content
content-type: application/json
```

## Apagar de novo (404)

```
curl -i -X DELETE http://127.0.0.1:8000/grupos/7
```

```
HTTP/1.1 404 Not Found
content-length: 34
content-type: application/json

{"detail":"Grupo não encontrado"}
```

## Método não permitido na coleção (405)

```
curl -i -X DELETE http://127.0.0.1:8000/grupos
```

```
HTTP/1.1 405 Method Not Allowed
allow: GET
content-length: 31
content-type: application/json

{"detail":"Method Not Allowed"}
```

## Rota que não existe (404)

```
curl -i http://127.0.0.1:8000/rota-que-nao-existe
```

```
HTTP/1.1 404 Not Found
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```
