# Módulo 17, Testes Automatizados

`SEM 05 // API RESTful Central`

---

## // Antes de começar

> **TRILHA VETERANO, MÓDULO BÔNUS**
> Este módulo faz parte da trilha veterano e é um **bônus**: ele aprofunda o que o Módulo 15 já usou, e não é necessário para o entregável da semana. Quem segue a trilha principal pode pular para o `entregavel.md`.

No Módulo 13 você conferiu a API com um roteiro de 17 requisições feitas à mão. Funciona, mas cansa, e ninguém repete 17 requisições depois de cada pequena mudança. Este módulo troca o roteiro por **testes automatizados**: pequenos programas que fazem as requisições, conferem as respostas e avisam se algo quebrou. Os testes estão em `example/api-limpa/tests/`.

## // O problema: mudar o código dá medo

Sem testes, cada alteração tem um risco escondido: você muda uma regra e, sem querer, quebra outra. Só descobre quando alguém reclama. Com testes, a resposta vem em menos de um segundo, no próprio terminal.

## // pytest e TestClient

> **PYTEST: EM PALAVRAS SIMPLES**
> É uma ferramenta que encontra e executa funções de teste. Todo arquivo chamado `test_*.py` e toda função chamada `test_*` são executados automaticamente. Um teste passa se nenhuma de suas conferências (`assert`) falhar.

> **TESTCLIENT: EM PALAVRAS SIMPLES**
> É um "cliente de mentira" que o FastAPI oferece para chamar a API **sem ligar um servidor**. Ele faz as requisições direto no código da aplicação, o que é rápido e não depende da rede.

## // Instalando

O `requirements.txt` da versão limpa tem três linhas:

```
fastapi[standard]>=0.143,<0.144
pytest
httpx2
```

O `httpx2` merece uma explicação. O `TestClient` do FastAPI precisa de uma biblioteca de requisições HTTP. Com a biblioteca `httpx` (instalada junto com o `fastapi[standard]`), o teste roda, mas o Python emite este aviso a cada execução:

```
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

O aviso pede para instalar o `httpx2`. Foi o que se fez: com ele instalado, o aviso desaparece e os testes passam normalmente.

## // O primeiro teste

Em `tests/test_materias.py`:

```python
def test_lista_as_seis_materias(client):
    assert len(client.get("/materias").json()) == 6
```

Um bom teste tem três momentos, conhecidos pela sigla em inglês **AAA**:

| Momento | Significado |
|---|---|
| **Arrange** (preparar) | O `client`, entregue pela fixture (veja a seguir) |
| **Act** (agir) | `client.get("/materias")` |
| **Assert** (conferir) | O `assert` |

O nome do teste é uma **frase** que descreve o que se espera. Quando ele falha, o nome já diz o que quebrou. Rode com `pytest -q`.

## // Fixtures: preparando o terreno

> **FIXTURE: EM PALAVRAS SIMPLES**
> É uma função que prepara algo de que os testes precisam (um cliente, dados limpos) e o entrega a quem pedir. Qualquer teste que declare um parâmetro com o nome da fixture a recebe.

O `tests/conftest.py` guarda as fixtures compartilhadas:

```python
@pytest.fixture
def servicos():
    """Os casos de uso, com repositórios novos em memória: sem HTTP, sem FastAPI."""
    materias = novo_repositorio_de_materias()
    grupos = novo_repositorio_de_grupos()
    return ServicoGrupos(grupos, materias), ServicoMaterias(materias)


@pytest.fixture
def client(servicos):
    """Um cliente HTTP cujos serviços foram trocados por versões com dados limpos."""
    servico_grupos, servico_materias = servicos
    app.dependency_overrides[dependencias.obter_servico_grupos] = lambda: servico_grupos
    app.dependency_overrides[dependencias.obter_servico_materias] = lambda: servico_materias
    yield TestClient(app)
    app.dependency_overrides.clear()
```

O que cada parte faz:

| Parte | O que faz |
|---|---|
| `@pytest.fixture` | Marca a função como fixture |
| `def servicos()` | Cria **repositórios novos** a cada teste: nenhum teste herda os dados de outro |
| `app.dependency_overrides[...]` | Troca, só durante o teste, a dependência da raiz de composição por uma versão com dados limpos |
| `yield TestClient(app)` | Entrega o cliente ao teste, e o código depois do `yield` roda quando o teste termina |
| `.clear()` | Desfaz as trocas, deixando a API como estava |

O `dependency_overrides` é um recurso do FastAPI feito justamente para testes. Ele só é possível porque a arquitetura do Módulo 15 **entrega** o serviço às rotas por `Depends`, em vez de as rotas o criarem sozinhas.

## // A configuração

O arquivo `pytest.ini`, na raiz do projeto:

```
[pytest]
pythonpath = .
testpaths = tests
```

O `pythonpath = .` faz a pasta do projeto entrar no caminho de importação, e é por isso que `from app import ...` funciona dentro dos testes. Sem essa linha, o comando `pytest` puro falha assim:

```
ImportError while loading conftest '.../tests/conftest.py'.
ModuleNotFoundError: No module named 'app'
```

## // Três tipos de teste

A suíte da API limpa tem 36 testes, em seis arquivos, e cada um responde a uma pergunta diferente:

| Arquivo | Testes | Pergunta que responde |
|---|---|---|
| `test_servico_sem_fastapi.py` | 7 | As **regras** funcionam, sem HTTP e sem FastAPI? |
| `test_arquitetura.py` | 3 | O núcleo continua **livre do framework**? |
| `test_api_grupos.py` | 9 | As **rotas** de grupos devolvem os códigos e os corpos certos? |
| `test_erros.py` | 9 | Todo erro sai no **formato único**? |
| `test_listagem.py` | 5 | **Filtros, ordenação e paginação** funcionam? |
| `test_materias.py` | 3 | As rotas de **matérias** funcionam? |

### > Testando uma regra, sem HTTP

```python
def test_nome_repetido_na_mesma_materia_e_recusado_sem_diferenciar_maiusculas(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(GrupoDuplicadoError):
        servico_grupos.criar("CÁLCULO PASSO A PASSO", materia_id=1)
```

O `pytest.raises` confere que o código **levanta** o erro esperado. Nenhuma requisição foi feita.

### > Testando uma rota

```python
def test_cria_um_grupo(client):
    resposta = client.post("/grupos", json=NOVO)
    assert resposta.status_code == 201
    assert resposta.headers["location"] == "/grupos/7"
    assert resposta.json()["grupo_id"] == 7
```

### > Testando uma resposta sem corpo

```python
def test_delete_devolve_204_sem_corpo_e_depois_404(client):
    resposta = client.delete("/grupos/2")
    assert resposta.status_code == 204
    assert resposta.content == b""
    assert client.delete("/grupos/2").status_code == 404
```

### > Testando o bug do PATCH com null

```python
def test_patch_com_null_nos_outros_campos_devolve_422_e_nao_corrompe(client):
    for campo in ("nome_grupo", "materia_id", "max_participantes"):
        resposta = client.patch("/grupos/1", json={campo: None})
        assert resposta.status_code == 422
        assert resposta.json()["detalhes"][0]["campo"] == f"body.{campo}"
    assert client.get("/grupos").status_code == 200  # a lista inteira continua saudável
    assert client.get("/grupos/1").json()["max_participantes"] == 6
```

Este teste é o "seguro de vida" do problema do Módulo 09: se alguém um dia remover o validador, ele falha na hora. É um bom exemplo de por que **todo bug corrigido vira um teste**.

### > Testando um erro inesperado

```python
def test_erro_inesperado_vira_500_em_json_sem_vazar_detalhes():
    app_de_teste = FastAPI()
    registrar_tratadores(app_de_teste)

    @app_de_teste.get("/quebra")
    def quebra():
        raise RuntimeError("detalhe interno secreto")

    resposta = TestClient(app_de_teste, raise_server_exceptions=False).get("/quebra")
    assert resposta.status_code == 500
    assert resposta.json() == {"erro": "erro_interno", "mensagem": "Erro interno do servidor", "detalhes": None}
    assert "secreto" not in resposta.text
```

O teste cria uma **aplicação mínima só para ele**, com uma rota que quebra de propósito, já que a API real não tem nenhuma. Repare no `raise_server_exceptions=False` (Módulo 16).

## // Rodando a suíte

```
pytest -q
```

```
....................................                                     [100%]
36 passed in 0.22s
```

Trinta e seis testes em menos de um quarto de segundo. É o que substitui as 17 requisições manuais, e mais várias, a cada mudança.

## // Lendo uma falha

Um teste que falha é uma **informação útil**, e não um problema. Veja um teste escrito com uma expectativa errada de propósito (o grupo 3 tem limite 8, e o teste espera 10):

```python
def test_grupo_3_tem_limite_10(client):
    resposta = client.get("/grupos/3")
    assert resposta.status_code == 200
    assert resposta.json()["max_participantes"] == 10
```

```
    def test_grupo_3_tem_limite_10(client):
        resposta = client.get("/grupos/3")
        assert resposta.status_code == 200
>       assert resposta.json()["max_participantes"] == 10
E       assert 8 == 10

tests/test_falha.py:4: AssertionError
FAILED tests/test_falha.py::test_grupo_3_tem_limite_10 - assert 8 == 10
1 failed in 0.03s
```

O sinal `>` marca a linha que falhou, e o `assert 8 == 10` mostra o valor real (8) contra o esperado (10). A pergunta passa a ser: o código está errado, ou o teste está? Aqui, o teste.

## // Bom exemplo × mau exemplo

**Mau exemplo**: um teste que depende de outro ter rodado antes:

```python
def test_cria_grupo(client):
    client.post("/grupos", json=NOVO)

def test_busca_o_grupo_criado(client):
    assert client.get("/grupos/7").status_code == 200   # só funciona se o teste anterior rodou
```

**Bom exemplo**: cada teste cria o que precisa:

```python
def test_busca_o_grupo_criado(client):
    client.post("/grupos", json=NOVO)
    assert client.get("/grupos/7").status_code == 200
```

Somado à fixture que cria repositórios novos, cada teste começa do zero e pode rodar sozinho.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` ao rodar `pytest` | Falta o `pythonpath = .` no `pytest.ini` | Crie o `pytest.ini` como mostrado |
| Um teste passa sozinho e falha na suíte | Ele depende de dados deixados por outro teste | Use a fixture com repositórios novos, e faça cada teste criar o que precisa |
| O aviso `StarletteDeprecationWarning` em todo teste | Está instalado só o `httpx` | Instale o `httpx2` |
| O `pytest` não acha os testes | O arquivo ou a função não começa com `test_` | Renomeie para `test_*.py` e `def test_...` |
| O teste do `POST` devolve `422` mesmo com o corpo certo | Foi usado `content=` em vez de `json=` | Use `json=` para enviar JSON com o cabeçalho correto |
| O teste do `500` levanta a exceção | O `TestClient` re-levanta erros inesperados | Use `raise_server_exceptions=False` |
| Um teste "interfere" nos seguintes | O `dependency_overrides` não foi limpo | Use `yield` na fixture e `.clear()` depois |

## // Prática guiada

1. Instale o `pytest` e o `httpx2`, e crie o `pytest.ini`, a pasta `tests` e o `conftest.py` com as duas fixtures.
2. Escreva `test_materias.py` com os três testes de matérias e rode `pytest -q`.
3. Escreva um teste de regra, sem HTTP, usando a fixture `servicos`.
4. Escreva o teste de `POST` com `201` e `Location`, e o de `409` ao repetir.
5. Provoque uma falha de propósito, leia a mensagem e corrija.

## // Pratique sozinho

> **DESAFIO**
> Escreva três testes novos: (a) `GET /grupos?materia_id=99` devolve `200` com lista vazia; (b) `PATCH /grupos/1` com o `nome_grupo` de **outro** grupo da mesma matéria devolve `409` (crie antes um grupo na matéria 1 para ter o conflito); (c) `POST /grupos` com `max_participantes` igual a 51 devolve `422` com o campo `body.max_participantes`. Rode a suíte e confirme que todos passam.

## // Aplicando no projeto da semana

1. Se você seguiu a trilha veterano, complete a pasta `tests` da sua API com pelo menos um teste para cada rota e um para cada regra.
2. Rode `pytest -q` antes de cada commit.
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Adiciona testes automatizados da API"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Por que a fixture `servicos` cria repositórios **novos** a cada teste, em vez de reaproveitar os mesmos?

Resposta: porque os testes podem criar, alterar e apagar grupos. Se todos usassem o mesmo repositório, o que um teste fizesse ficaria para o seguinte, e o resultado dependeria da **ordem** em que eles rodam. Com repositórios novos, todo teste começa do mesmo estado inicial (seis grupos, seis matérias), e pode rodar sozinho, em qualquer ordem.

## // Resumo do módulo

- [ ] Sei o que é um teste automatizado, e o que fazem o `pytest` e o `TestClient`.
- [ ] Sei escrever um teste com preparar, agir e conferir.
- [ ] Sei criar fixtures, e usar `dependency_overrides` para trocar uma dependência.
- [ ] Sei configurar o `pytest.ini` com `pythonpath`.
- [ ] Sei testar regras sem HTTP, rotas, respostas sem corpo e erros.
- [ ] Sei transformar um bug corrigido em um teste, e ler a mensagem de uma falha.

---

**Próximo módulo:** `18-filtros-ordenacao-e-paginacao.md`, o outro módulo bônus da trilha veterano.

`Material de Estudo // Coffee & Code`
