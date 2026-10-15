# Módulo 13, Projeto Guiado: A API de Grupos de Estudo

Português · [English](../docs-eng/13-guided-project.md)

`SEM 05 // API RESTful Central`

---

## // Para que serve este módulo

Nenhum conceito novo aparece aqui. Este módulo junta, em ordem, tudo o que os Módulos 01 a 12 ensinaram, e termina com o entregável da semana: uma API local em FastAPI com o CRUD completo de grupos, validação, códigos de status corretos e Swagger documentado.

## // Etapa 1, Preparar a pasta e o ambiente (Módulo 05)

Na pasta `api-grupos`, confirme que o ambiente virtual existe e está **ativo** (o terminal mostra `(.venv)`). Confirme a versão com `python --version`: precisa ser 3.10 ou superior.

## // Etapa 2, Instalar o FastAPI (Módulo 07)

O arquivo `requirements.txt` deve ter esta linha:

```
fastapi[standard]>=0.143,<0.144
```

```
pip install -r requirements.txt
fastapi --version
```

## // Etapa 3, Os dados (Módulo 06 e 10)

Crie o `dados.py` com as seis matérias e os seis grupos de exemplo, e o `CONTADOR_GRUPOS` começando em 7. O arquivo completo está em `example/api-basica/dados.py`.

## // Etapa 4, Os modelos (Módulo 09)

Crie o `schemas.py` com `MateriaOut`, `GrupoBase`, `GrupoCreate`, `GrupoUpdate`, `GrupoPatch` e `GrupoOut`. Confira que ele importa: `python -c "import schemas"`.

## // Etapa 5, As rotas de leitura (Módulo 10)

No `main.py`, crie a aplicação com `title`, `description` e `version`, e escreva `GET /materias`, `GET /materias/{materia_id}`, `GET /grupos` (com `q` e `materia_id`) e `GET /grupos/{grupo_id}`, usando `buscar_grupo_ou_404`. Remova as rotas de exemplo dos Módulos 07 e 08.

Ligue o servidor (`fastapi dev main.py`) e confira no `/docs` se as quatro rotas apareceram.

## // Etapa 6, As rotas de escrita (Módulo 11)

Escreva as funções `conferir_materia` e `conferir_nome_livre`, e as rotas `POST /grupos` (201 e `Location`), `PUT /grupos/{grupo_id}`, `PATCH /grupos/{grupo_id}` e `DELETE /grupos/{grupo_id}` (204).

## // Etapa 7, A documentação (Módulo 12)

Acrescente `summary` em todas as rotas, `openapi_tags` com a descrição de `materias` e `grupos`, e `responses` nas rotas que podem devolver `404`, `409` ou `422`.

## // Etapa 8, O roteiro de testes

Pelo Swagger, execute estas 17 requisições, **nesta ordem**, e confira o resultado esperado. Todos os resultados abaixo foram obtidos da API em execução.

| # | Requisição | Resultado esperado |
|---|---|---|
| 1 | `GET /grupos` | `200`, seis grupos |
| 2 | `GET /grupos?q=prática` | `200`, só `Estruturas na prática` |
| 3 | `GET /grupos?materia_id=1` | `200`, só `Cálculo passo a passo` |
| 4 | `GET /grupos/3` | `200`, o grupo `Modelagem e SQL` |
| 5 | `GET /grupos/99` | `404`, `Grupo não encontrado` |
| 6 | `GET /grupos/abc` | `422`, `int_parsing`, com `loc` apontando `path` e `grupo_id` |
| 7 | `POST /grupos` com `Cálculo II na prática`, matéria 1, limite 5 | `201`, `grupo_id` 7, cabeçalho `Location: /grupos/7` |
| 8 | O mesmo `POST` de novo | `409`, `Já existe um grupo com esse nome nessa matéria` |
| 9 | `POST /grupos` com `materia_id` 99 | `422`, `A matéria 99 não existe` |
| 10 | `POST /grupos` com `nome_grupo` igual a `ab` | `422`, `string_too_short` |
| 11 | `PUT /grupos/7` com `Cálculo II revisado`, matéria 1, limite 6 | `200`, o grupo substituído |
| 12 | `PATCH /grupos/7` com `max_participantes` 8 | `200`, só o limite mudou |
| 13 | `PATCH /grupos/7` com `nome_grupo` igual a `null` | `422`, `loc` apontando `body` e `nome_grupo` |
| 14 | `DELETE /grupos/7` | `204`, sem corpo |
| 15 | `DELETE /grupos/7` de novo | `404` |
| 16 | `DELETE /grupos` | `405 Method Not Allowed` |
| 17 | `GET /materias/99` | `404`, `Matéria não encontrada` |

Se todas as 17 baterem, a API está correta.

> **OS DADOS VOLTAM AO INÍCIO**
> No modo `fastapi dev`, o servidor reinicia sempre que você **salva um arquivo**, e a cada reinício os dados voltam ao estado inicial. Isso é esperado, porque tudo vive em memória. Se um teste depender de um grupo que você criou, faça a criação e o teste antes de editar qualquer arquivo.

## // Etapa 9, Fechamento do projeto

1. Rode `pip freeze` e confira se as versões batem com as da instalação (o `requirements.txt` fixa só a faixa do FastAPI).
2. No `README.md`, descreva em poucas linhas: o que a API faz, como instalar (`pip install -r requirements.txt`), como rodar (`fastapi dev main.py`) e onde fica a documentação (`/docs`).
3. Confirme que a pasta `.venv` está fora do repositório (`.gitignore`), se você usa Git.
4. Se você versiona o projeto com Git, faça um commit: `git commit -m "Finaliza a API de grupos de estudo"`.

## // Checklist de fechamento

- [ ] A API liga com `fastapi dev main.py` sem nenhum erro no terminal.
- [ ] As 8 rotas existem e aparecem no `/docs`, agrupadas por `materias` e `grupos`.
- [ ] As 17 requisições do roteiro devolvem o resultado esperado.
- [ ] Os códigos de status estão corretos: `201` no `POST`, `204` no `DELETE`, `404`, `409` e `422` nos erros.
- [ ] Todas as rotas têm `summary`, e as que podem falhar têm `responses`.
- [ ] O `requirements.txt` fixa a faixa de versões do FastAPI.
- [ ] O `README.md` explica como instalar e rodar.

## // Erros comuns ao juntar tudo

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `ModuleNotFoundError: No module named 'dados'` | O arquivo `dados.py` não está na mesma pasta do `main.py`, ou o servidor foi iniciado em outra pasta | Rode `fastapi dev main.py` na pasta que contém os dois arquivos |
| `ImportError` ao importar de `schemas` | Um modelo foi digitado errado, ou falta no arquivo | Confira os nomes importados no `main.py` |
| Uma rota do roteiro devolve `200` onde se esperava `201` | Faltou o `status_code` no decorador | Confira o `status_code` de `POST` e `DELETE` |
| `422` em todo `POST`, `PUT` ou `PATCH` pelo `curl` | Faltou o `Content-Type` | Acrescente `-H "Content-Type: application/json"` |
| O grupo criado "sumiu" | O servidor reiniciou ao salvar um arquivo | É o esperado: os dados vivem em memória |
| A rota `/grupos/novo` (se criada) nunca é alcançada | A rota com parâmetro foi declarada antes | Declare as rotas fixas antes das rotas com parâmetro |

## // Aplicando no projeto da semana

Esta é a aplicação: não existe uma atividade separada. Ao final deste módulo, a API deve passar pelo checklist do `entregavel.md`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Se você tivesse que explicar para alguém, em três frases, o caminho de um `POST /grupos` desde o pedido até a resposta, o que diria?

Resposta possível: o FastAPI lê o corpo JSON, confere o `Content-Type` e valida os campos com o modelo `GrupoCreate`; se algo estiver errado, devolve `422` sem nem chamar a função. Se estiver tudo certo, a função confere as regras de negócio (a matéria existe? o nome está livre?), gera o identificador, guarda o grupo e devolve `201` com o grupo e o cabeçalho `Location`. Em qualquer ponto em que uma regra falhe, o `HTTPException` interrompe a função e vira uma resposta com o código certo.

## // Resumo do módulo

- [ ] Consigo repetir, de memória, a sequência de etapas usada para montar a API.
- [ ] A minha API passa pelas 17 requisições do roteiro de testes.
- [ ] O checklist de fechamento está completo.

---

**Próximo módulo:** `14-organizando-uma-api-em-camadas.md` para a trilha veterano, ou `entregavel.md` para a revisão final de quem segue a trilha principal.

`Material de Estudo // Coffee & Code`
