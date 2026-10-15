# Exemplos executáveis, Semana 05

Esta pasta reúne tudo que pode ser executado nesta semana. É referência, e não gabarito obrigatório: a sua API precisa aplicar os mesmos conceitos, não ser igual a esta.

## Ambiente em que tudo foi testado

| Item | Versão |
|---|---|
| Python | 3.12.3 (o FastAPI exige 3.10 ou superior) |
| FastAPI | 0.143.0 |
| Starlette | 1.7.0 |
| Pydantic | 2.13.5 |
| Uvicorn | 0.54.0 |
| pytest | 9.1.1 |
| httpx2 | 2.13.1 |
| Sistema | Linux. **Não foi testado no Windows nem no macOS** |

A documentação oficial do FastAPI foi consultada em **08/10/2026**. O FastAPI é uma biblioteca de versão `0.x` e muda com frequência: se algo divergir do que está aqui, a documentação oficial é a referência.

## Qual pasta usar

| Pasta | Módulos | O que é |
|---|---|---|
| `api-basica/` | 07 a 13 | A API da trilha principal: três arquivos |
| `api-em-pacotes/` | 14 | A mesma API dividida em pacotes e routers. As regras ainda importam o FastAPI |
| `api-limpa/` | 15 a 18 | Clean Architecture, tratamento global de erros, paginação e 36 testes |

As três têm o mesmo comportamento para o cliente, com uma diferença: a `api-limpa` devolve **todos** os erros no formato único `erro`, `mensagem` e `detalhes` (Módulo 16), e a `api-basica` e a `api-em-pacotes` usam o formato padrão do FastAPI (`detail`).

## `api-basica/`: a trilha principal

```
api-basica/
├── main.py
├── dados.py
├── schemas.py
└── requirements.txt
```

Para rodar, dentro da pasta `api-basica`:

```
python3 -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py
```

A documentação abre em `http://127.0.0.1:8000/docs`. Use `fastapi dev`, e não `fastapi run`: o `dev` atende só o seu computador, e o `run` atende toda a rede.

## `api-em-pacotes/`: o Módulo 14

```
api-em-pacotes/
├── app/
│   ├── main.py
│   ├── dados.py
│   ├── schemas.py
│   ├── regras.py
│   └── routers/
│       ├── grupos.py
│       └── materias.py
└── requirements.txt
```

Para rodar, dentro da pasta `api-em-pacotes`: os mesmos comandos, trocando o último por `fastapi dev app/main.py`.

## `api-limpa/`: os Módulos 15 a 18

```
api-limpa/
├── app/
│   ├── main.py
│   ├── dominio/            entidades, erros e interfaces dos repositórios
│   ├── aplicacao/          os casos de uso
│   ├── infraestrutura/     o repositório em memória
│   └── api/                rotas, modelos, dependências e tratamento de erros
├── tests/                  36 testes
├── pytest.ini
└── requirements.txt
```

Para rodar, dentro da pasta `api-limpa`:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
pytest -q
```

## `exemplos-curl.md`

As requisições com `curl` usadas nos módulos, com as respostas reais de uma execução da `api-basica`. Execute na ordem.

## Regras de segurança

- Rode a API sempre com `fastapi dev`. Ela não tem nenhum controle de acesso.
- O ambiente virtual (`.venv`) nunca vai para o repositório.
- Os dados vivem em memória e voltam ao estado inicial a cada reinício do servidor.
