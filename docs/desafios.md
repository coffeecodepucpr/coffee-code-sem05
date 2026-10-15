# Desafios, Semana 05

Desafios opcionais, organizados pelos módulos da semana. Nenhum é obrigatório para a entrega básica; veja `entregavel.md` para o que é obrigatório. Use estes desafios se terminou os módulos principais e quer se aprofundar, ou se quer deixar a API mais robusta.

---

## // HTTP, métodos e status codes (Módulos 01 a 04)

**Se você está começando**
- Abra as ferramentas do navegador (tecla F12, aba Rede) em três sites diferentes e anote, para cada um, três requisições com o método, o código de status e o `Content-Type`.
- Escolha um sistema do seu dia a dia (uma loja online, uma rede social) e escreva as rotas REST dos seus principais recursos, com os métodos e os códigos de sucesso de cada uma.

**Se você já tem experiência**
- Pesquise o código `429 Too Many Requests` e explique em que situação uma API deveria devolvê-lo.
- Pesquise a diferença entre `401 Unauthorized` e `403 Forbidden`, e escreva um exemplo de cada para o recurso `/grupos`.

---

## // Python (Módulos 05 e 06)

**Se você está começando**
- Escreva uma função `agrupar_por_materia(grupos)` que receba a lista de grupos e devolva um dicionário em que a chave é o `materia_id` e o valor é a lista dos grupos daquela matéria.
- Escreva uma função que receba o dicionário `GRUPOS` e devolva o grupo com mais participantes, ou `None` se o dicionário estiver vazio.

**Se você já tem experiência**
- Pesquise a diferença entre `dict.get`, `dict.setdefault` e `collections.defaultdict`, e reescreva a função `agrupar_por_materia` com cada um.
- Pesquise o que são *type hints* genéricos (`list[dict]`, `dict[int, dict]`) e acrescente-os a todas as funções de `dados.py`.

---

## // FastAPI, rotas e Pydantic (Módulos 07 a 09)

**Se você está começando**
- Acrescente uma rota `GET /grupos/{grupo_id}/vagas` que devolva só o `max_participantes` de um grupo e `404` se ele não existir.
- Acrescente uma validação ao modelo `GrupoBase` que recuse nomes formados só por espaços (dica: pesquise o decorador `field_validator` do Pydantic).

**Se você já tem experiência**
- Pesquise a diferença entre `response_model_exclude_unset` e `response_model_exclude_none`, e use um dos dois para esconder a `descricao` quando ela for `null`.
- Pesquise como o Pydantic trata campos extras enviados no corpo (`extra="forbid"`) e faça o `POST /grupos` recusar campos desconhecidos.

---

## // CRUD e Swagger (Módulos 10 a 12)

**Se você está começando**
- Acrescente `GET /materias/{materia_id}/grupos`, que devolva os grupos de uma matéria (e `404` se a matéria não existir).
- Documente todas as rotas com um exemplo de resposta de sucesso, usando o parâmetro `responses`.

**Se você já tem experiência**
- Pesquise o parâmetro `operation_id` do decorador e reescreva os identificadores das operações para nomes mais legíveis.
- Pesquise como configurar o Swagger para carregar os arquivos do próprio servidor, sem depender de internet (a documentação do FastAPI chama isso de arquivos estáticos para `/docs`), e avalie o trabalho que isso exige.

---

## // Trilha veterano (Módulos 14 a 18)

- Acrescente à `api-limpa` um segundo repositório, `RepositorioGruposEmArquivo`, que guarde os grupos em um arquivo JSON, e troque um pelo outro **só** na raiz de composição (`dependencias.py`). Confira que nenhum arquivo de `dominio/` ou `aplicacao/` precisou mudar.
- Escreva um teste de arquitetura que garanta que a `aplicacao` não importa a `infraestrutura`, e prove que ele funciona fazendo a mutação (acrescente o import proibido e veja o teste falhar).
- Registre um tratador para um erro que você mesmo criou (por exemplo, `LimiteExcedidoError`), e confirme que o formato `erro`, `mensagem` e `detalhes` se mantém.
- Pesquise o que é um *middleware* no FastAPI e escreva um que registre no log o método, o caminho e o tempo de cada requisição.
- Acrescente um filtro `min_vagas` à listagem e crie um teste para ele.
- Pesquise por que a paginação por `offset` pode pular ou repetir itens quando os dados mudam entre uma página e outra, e o que é a paginação por cursor.
- Pesquise o formato **RFC 9457** (*Problem Details for HTTP APIs*) e compare com o formato único de erro do Módulo 16.

---

## // Desafio geral (todos)

Escreva um arquivo `docs/decisoes.md` com as cinco principais decisões de design da sua API, cada uma em duas frases: o que você decidiu e por quê. Exemplos: por que `PATCH` e `PUT` coexistem, por que um nome repetido devolve `409` e não `422`, por que os identificadores vêm de um contador. Se você conseguir justificar cada uma sem olhar o material, a sua API está em um bom nível.
