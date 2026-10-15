# Coffee & Code | SEM 05 | API RESTful Central (Parte 1: CRUD)

Português · [English](README.en.md)

```text
> module: sem-05
> tema: api restful central (crud)
> status: online
> coffee loaded
```

Material da **Semana 05** da trilha do Coffee & Code, clube de tecnologia fundado por estudantes de Engenharia de Software da PUCPR e aberto a todos que querem aprender construindo.

Esta semana leva uma pessoa que nunca construiu uma API até uma API de CRUD funcionando, validada e documentada com o Swagger: Python, FastAPI, métodos HTTP e status codes.

> **Semana independente:** ela não exige nenhuma outra semana do clube. Python, HTTP e o projeto de exemplo são apresentados do zero.

> **Sobre o idioma:** o material em inglês fica em [`docs-eng/`](docs-eng/), com a mesma estrutura de [`docs/`](docs/); os READMEs têm versão em inglês com o sufixo `.en.md`.

## Por onde começar

**[docs/00-comece-aqui.md](docs/00-comece-aqui.md)**: leia este primeiro. Ele apresenta o panorama da semana e a ideia de uma API central.

Depois, siga os módulos na ordem. Os módulos `01` a `13` formam a trilha principal:

| # | Módulo | Sobre |
|---|---|---|
| 01 | [O que é uma API REST](docs/01-o-que-e-uma-api-rest.md) | API, recurso, JSON e as ideias do REST |
| 02 | [HTTP na prática](docs/02-http-na-pratica.md) | Requisição, resposta, URL e `Content-Type` |
| 03 | [Métodos HTTP](docs/03-metodos-http.md) | `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, seguro e idempotente |
| 04 | [Status codes](docs/04-status-codes.md) | As famílias de status e os códigos de um CRUD |
| 05 | [Python: ambiente, tipos e decisões](docs/05-python-ambiente-tipos-e-decisoes.md) | Ambiente virtual, tipos, `if` e repetições |
| 06 | [Python: funções, listas e dicionários](docs/06-python-funcoes-listas-e-dicionarios.md) | Funções, listas, dicionários e dicas de tipo |
| 07 | [Sua primeira API com FastAPI](docs/07-sua-primeira-api-com-fastapi.md) | Instalação, `fastapi dev` e o Swagger |
| 08 | [Rotas e parâmetros](docs/08-rotas-e-parametros.md) | Parâmetros de caminho e de consulta, validação |
| 09 | [Modelos com Pydantic](docs/09-modelos-com-pydantic.md) | Modelos, corpo da requisição e `response_model` |
| 10 | [CRUD: lendo dados](docs/10-crud-lendo-dados.md) | `GET` de lista e de um item, e o 404 |
| 11 | [CRUD: criar, atualizar e apagar](docs/11-crud-criar-atualizar-e-apagar.md) | `POST`, `PUT`, `PATCH` e `DELETE`, com 201, 204 e 409 |
| 12 | [Swagger na prática](docs/12-swagger-na-pratica.md) | OpenAPI, Swagger UI e como documentar |
| 13 | [Projeto guiado](docs/13-projeto-guiado.md) | A API completa, com um roteiro de 17 testes |

Os módulos `14` a `16` são a **trilha veterano**, e os módulos `17` e `18` são bônus dessa trilha. Todos são opcionais e podem ser lidos depois:

| # | Módulo | Sobre |
|---|---|---|
| 14 | [Organizando uma API em camadas](docs/14-organizando-uma-api-em-camadas.md) | Pacotes, `APIRouter` e camadas |
| 15 | [Clean Architecture no FastAPI](docs/15-clean-architecture-no-fastapi.md) | Domínio, aplicação, infraestrutura e API |
| 16 | [Tratamento global de erros](docs/16-tratamento-global-de-erros.md) | `exception_handler` e formato único de erro |
| 17 | [Testes automatizados](docs/17-testes-automatizados.md) | Bônus: `pytest`, `TestClient` e fixtures |
| 18 | [Filtros, ordenação e paginação](docs/18-filtros-ordenacao-e-paginacao.md) | Bônus: `Depends` e paginação |

E, para consultar quando precisar:

- [Exemplos executáveis](docs/example/README.md): as três versões da API, para consulta
- [Desafios](docs/desafios.md): opcionais, para ir além do pedido
- [Entregável](docs/entregavel.md): checklist final antes de fechar a semana

## Os exemplos executáveis

A pasta [`docs/example/`](docs/example/) tem três versões da API do Buscador de Grupos de Estudo:

- `api-basica/`: a API da trilha principal.
- `api-em-pacotes/`: a versão da trilha veterano, dividida em pacotes.
- `api-limpa/`: a versão com Clean Architecture, tratamento global de erros e testes.

Todas foram executadas, e as respostas citadas nos módulos vêm dessas execuções. Veja o [README da pasta](docs/example/README.md) para instalar e rodar.

É material de **consulta, não gabarito**: o exemplo serve para você ver uma solução possível quando travar, não para copiar.

## O entregável

Ao final da Semana 05, o repositório do **seu projeto** (não este aqui) deve ter uma pasta `api-grupos` com:

```text
api-grupos/
├── main.py
├── dados.py
├── schemas.py
├── requirements.txt
└── README.md         ← como instalar e rodar
```

A API precisa rodar localmente com `fastapi dev main.py`, ter as 8 rotas do CRUD com os métodos e status codes corretos, validar os dados com Pydantic e abrir a documentação em `/docs`.

O checklist completo está em [docs/entregavel.md](docs/entregavel.md).

## Entregas da turma

Ainda não há entregas da Semana 05. Quer ser a primeira pessoa? Veja [como entregar](entregas/README.md).

## Versões e data de consulta

Material verificado com **FastAPI 0.143.0**, Pydantic 2.13.5, Starlette 1.7.0, Uvicorn 0.54.0 e Python 3.12.3. A documentação oficial do FastAPI foi consultada em **08/10/2026**. O FastAPI é uma biblioteca de versão `0.x` e muda com frequência: se algo divergir do que está aqui, a documentação oficial é a referência.

## Projeto contínuo

Todos os módulos usam o mesmo projeto fictício do clube: o **Buscador de Grupos de Estudo**, uma aplicação em que estudantes procuram grupos de estudo por matéria. A API desta semana cuida dos grupos e das matérias. Se você tem um projeto próprio, o raciocínio de cada módulo se aplica da mesma forma: só troque o nome.

## Como funciona

O Coffee & Code é **100% online**. Cada módulo foi escrito para ser autossuficiente: você estuda no seu ritmo, pode avançar mais rápido, voltar em semanas anteriores e consultar o material durante o projeto.

Os encontros semanais, também online, existem para tirar dúvidas, revisar conceitos, programar junto e mostrar o que você produziu, **não para dar aula**:

- **quarta-feira**: 20h00 às 21h30
- **sábado**: 10h00 às 11h30

Os dois trabalham o mesmo conteúdo. Escolha o que couber melhor na sua semana, e não precisa ficar o horário inteiro na call.

## Travou?

Chega no encontro ou no Discord com uma pergunta específica. `"minha rota devolve 422, já conferi o modelo e o corpo da requisição"` costuma ser resolvido muito mais rápido do que `"minha API não funciona"`.

E lembra: não saber alguma coisa não é problema. Saber pesquisar faz parte da área.

## Diagramas

Todos os diagramas usados nos módulos estão em [`docs/assets/`](docs/assets/), em formato SVG.

## Semanas anteriores

- [SEM 01: Kickoff & Design System](https://github.com/coffeecodepucpr/coffee-code-sem01)
- [SEM 02: Interface Web (Parte 1: Layout)](https://github.com/coffeecodepucpr/coffee-code-sem02)
- [SEM 03: Interface Web (Parte 2: Dinâmica)](https://github.com/coffeecodepucpr/coffee-code-sem03)
- [SEM 04: Modelagem de Dados](https://github.com/coffeecodepucpr/coffee-code-sem04)

Trilha completa e próximas semanas: [perfil do Coffee & Code](https://github.com/coffeecodepucpr)

---

```text
HTTP 418: I'm a teapot
> ready to code
```
