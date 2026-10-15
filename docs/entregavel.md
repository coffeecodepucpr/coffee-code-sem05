# Entregável, Semana 05

Português · [English](../docs-eng/deliverable.md)

`SEM 05 // API RESTful Central`

Use este arquivo como checklist final antes de considerar a Semana 05 concluída. Ele reúne o que é **obrigatório**; os desafios extras em `desafios.md` e os Módulos 14 a 18 da trilha veterano são opcionais.

## // O que você deve ter em mãos agora

Se você seguiu os módulos em ordem, a sua pasta `api-grupos` deve conter: o `main.py`, o `dados.py`, o `schemas.py`, o `requirements.txt` e um `README.md`. A API deve rodar localmente com `fastapi dev main.py`, e a documentação deve abrir em `/docs`.

## // Checklist do entregável

### > Ambiente e execução

- [ ] O projeto tem um ambiente virtual, e o `.venv` não está no repositório (se você usa Git).
- [ ] O `requirements.txt` fixa a faixa de versões do FastAPI (`fastapi[standard]>=0.143,<0.144`).
- [ ] A API liga com `fastapi dev main.py`, sem nenhum erro no terminal.
- [ ] O `README.md` explica como instalar (`pip install -r requirements.txt`) e como rodar.

### > Rotas e métodos

- [ ] Existem as 8 rotas: `GET`, `POST`, `PUT`, `PATCH` e `DELETE` para os grupos, e `GET` para a lista e para um item de matérias.
- [ ] Cada rota usa o método HTTP adequado à ação.
- [ ] As rotas usam substantivos no plural e o identificador no caminho (`/grupos/{grupo_id}`).

### > Códigos de status

- [ ] `POST /grupos` devolve `201` e o cabeçalho `Location`.
- [ ] `DELETE /grupos/{grupo_id}` devolve `204`, sem corpo.
- [ ] Um grupo inexistente devolve `404` com uma mensagem clara.
- [ ] Um nome repetido na mesma matéria devolve `409`.
- [ ] Dados inválidos e uma matéria inexistente devolvem `422`.
- [ ] Nenhuma rota devolve `200` com uma mensagem de erro no corpo.

### > Validação e regras

- [ ] Os modelos Pydantic validam o nome (3 a 60 caracteres), a matéria e o limite (2 a 50).
- [ ] `PUT` substitui o grupo inteiro e `PATCH` altera só os campos enviados.
- [ ] `PATCH` com `null` em `nome_grupo`, `materia_id` ou `max_participantes` devolve `422`, e não corrompe o grupo.
- [ ] O identificador e a data de criação são gerados pela API, e não aceitos do cliente.

### > Documentação

- [ ] A aplicação tem `title`, `description` e `version`.
- [ ] Todas as rotas têm `summary`, e as que podem falhar declaram os `responses`.
- [ ] O `/docs` abre, e todas as rotas funcionam pelo **Try it out**.

### > Trilha veterano (opcional)

- [ ] A API está dividida em pacotes, com `APIRouter` por recurso.
- [ ] As regras de negócio **não importam** o FastAPI (Clean Architecture), e um teste confere isso.
- [ ] Os erros de domínio são traduzidos em **um único lugar**, com um formato único de erro.
- [ ] (Bônus) A suíte de testes passa com `pytest -q`.
- [ ] (Bônus) A listagem tem filtros, ordenação, paginação e o cabeçalho `X-Total-Count`.

## // O que NÃO é esperado nesta semana

- Não é esperado nenhum banco de dados: os dados ficam em memória e voltam ao estado inicial quando o servidor reinicia.
- Não é esperado login, permissões nem qualquer controle de acesso.
- Não é esperado publicar a API na internet. Use sempre `fastapi dev`, que atende só o seu computador.
- Não é esperada nenhuma tela ligada à API.

> **A LÓGICA CORRETA VALE MAIS QUE POLIMENTO**
> Uma API com poucas rotas, que devolve o código de status certo em cada situação e recusa dados inválidos com mensagens claras, vale mais nesta avaliação do que uma API cheia de recursos que responde `200` para tudo. O que está sendo avaliado esta semana é o comportamento correto.

## // Como revisar antes de entregar

> **O TESTE MAIS IMPORTANTE DESTA SEMANA**
> Em uma pasta nova e vazia, copie só os arquivos do projeto (sem o `.venv`), crie um ambiente virtual, rode `pip install -r requirements.txt` e `fastapi dev main.py`. Depois, execute no Swagger as 17 requisições do roteiro do Módulo 13. Se tudo bater, a sua API é reproduzível por qualquer pessoa.

Se algum passo falhar, a mensagem de erro quase sempre aponta o arquivo e a linha exatos: volte ao módulo correspondente.

## // Onde tirar dúvidas

Os encontros semanais do Coffee & Code existem para isso. "A minha rota de `PATCH` devolve `422` mesmo com o corpo certo, já conferi o `Content-Type`" é muito mais rápido de resolver do que "a minha API não funciona". Inclua sempre o código de status, o corpo da resposta e a requisição que você fez.

Se quiser se aprofundar além do que foi pedido, veja `desafios.md` e a trilha veterano, nos Módulos 14 a 18.

Bom trabalho até aqui.

`Material de Estudo // Coffee & Code`
