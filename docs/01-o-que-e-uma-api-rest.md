# Módulo 01, O que é uma API REST

`SEM 05 // API RESTful Central`

---

## // Antes de começar

Este módulo não tem código. Ele apresenta as ideias que organizam tudo o que vem depois: o que é uma API, o que é um recurso, por que as rotas têm o formato que têm, e o que significa a palavra REST. Entender isso agora evita a sensação de estar decorando regras sem motivo.

## // O problema: programas precisam conversar

Uma tela de listagem de grupos precisa dos dados dos grupos. Mas os dados não moram na tela: moram em outro programa, em outro computador. Para que dois programas troquem informações, eles precisam combinar **como** pedir e **como** responder. Se cada sistema inventar o seu próprio jeito, cada tela nova exige aprender uma conversa nova. Uma API resolve isso definindo a conversa.

## // O que é uma API

> **API: EM PALAVRAS SIMPLES**
> *Application Programming Interface* é o conjunto de pedidos que um programa aceita receber e o formato das respostas que ele devolve. É o "cardápio" de um programa: lista o que dá para pedir, sem mostrar como a cozinha funciona.

Duas palavras ajudam a descrever quem participa dessa conversa:

| Papel | Quem é | No projeto |
|---|---|---|
| **Cliente** | Quem faz o pedido | O navegador, o Swagger, o `curl`, uma tela, outro programa |
| **Servidor** | Quem recebe o pedido e responde | A API que você vai construir |

O cliente sempre começa a conversa. O servidor nunca "chama" o cliente por conta própria: ele espera um pedido, responde e volta a esperar.

## // Recursos: as "coisas" que a API expõe

> **RECURSO: EM PALAVRAS SIMPLES**
> É uma "coisa" do sistema que tem um endereço próprio e pode ser consultada ou alterada. No projeto desta semana, os recursos são os **grupos** de estudo e as **matérias**.

Todo recurso tem um endereço, chamado de **URL** ou **rota**:

| Endereço | O que representa |
|---|---|
| `/grupos` | A coleção de todos os grupos |
| `/grupos/3` | O grupo de identificador 3 |
| `/materias` | A coleção de todas as matérias |
| `/materias/1` | A matéria de identificador 1 |

Repare no padrão: o nome do recurso fica **no plural** (`/grupos`), e, para apontar um item específico, acrescenta-se o identificador depois de uma barra.

## // JSON: a língua dos dados

Os dados viajam entre cliente e servidor como texto. O formato mais usado é o **JSON**:

```json
{
  "grupo_id": 3,
  "nome_grupo": "Modelagem e SQL",
  "materia_id": 3,
  "max_participantes": 8,
  "descricao": "Encontros online às terças e aos sábados"
}
```

> **JSON: EM PALAVRAS SIMPLES**
> É um formato de texto para representar dados. Um objeto fica entre chaves, cada informação é um par `"nome": valor`, e os pares são separados por vírgula. Os valores podem ser texto (entre aspas duplas), números, `true` ou `false`, `null`, listas (entre colchetes) ou outros objetos.

Quase toda linguagem de programação sabe ler e escrever JSON. É por isso que um cliente em qualquer linguagem consegue conversar com uma API escrita em Python.

## // O que significa REST

> **REST: EM PALAVRAS SIMPLES**
> É um estilo de desenhar APIs sobre o HTTP, baseado em recursos com endereço próprio e em um pequeno conjunto de ações padronizadas. Uma API que segue o estilo é chamada de *RESTful*.

REST não é uma biblioteca nem uma tecnologia: é um conjunto de ideias. As quatro que importam nesta semana:

1. **Tudo é um recurso com endereço.** Os grupos moram em `/grupos`, e não em um endereço como `/pegarTodosOsGrupos`.
2. **As ações são padronizadas.** Em vez de inventar um endereço para cada ação, usa-se o mesmo endereço com **métodos** diferentes (o Módulo 03 detalha).
3. **A resposta diz como foi.** Cada resposta traz um **código de status** que informa se deu certo e, se não deu, de quem foi a falha (o Módulo 04 detalha).
4. **Cada pedido é independente.** O servidor não "lembra" do pedido anterior. Tudo de que ele precisa para responder vem dentro do próprio pedido.

## // A API que você vai construir

Ao final da semana, a API do projeto terá estas rotas:

| Operação | Método | Rota |
|---|---|---|
| Listar os grupos | `GET` | `/grupos` |
| Buscar um grupo | `GET` | `/grupos/{grupo_id}` |
| Criar um grupo | `POST` | `/grupos` |
| Substituir um grupo | `PUT` | `/grupos/{grupo_id}` |
| Alterar parte de um grupo | `PATCH` | `/grupos/{grupo_id}` |
| Apagar um grupo | `DELETE` | `/grupos/{grupo_id}` |
| Listar as matérias | `GET` | `/materias` |
| Buscar uma matéria | `GET` | `/materias/{materia_id}` |

Os nomes entre chaves, como `{grupo_id}`, indicam o lugar onde entra o identificador. Os métodos e os verbos vão ficar claros nos próximos módulos.

## // Bom exemplo × mau exemplo

**Mau exemplo**: um endereço para cada ação, com o verbo dentro do nome:

| Rota | O que faz |
|---|---|
| `/listarGrupos` | Lista |
| `/criarGrupo` | Cria |
| `/apagarGrupo?id=3` | Apaga |

Com 20 recursos e 5 ações cada, surgem 100 endereços diferentes para decorar, e cada API nova inventa os seus.

**Bom exemplo**: um endereço por recurso, e a ação vem do método:

| Rota | Método | O que faz |
|---|---|---|
| `/grupos` | `GET` | Lista |
| `/grupos` | `POST` | Cria |
| `/grupos/3` | `DELETE` | Apaga |

Quem já conhece uma API REST consegue adivinhar boa parte de outra, porque todas seguem o mesmo padrão.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Achar que API é o mesmo que "site" | As duas coisas respondem a endereços | Um site devolve páginas para pessoas; uma API devolve dados para programas |
| Achar que REST é uma tecnologia que se instala | O nome parece de ferramenta | REST é um estilo de desenho, e o FastAPI é uma ferramenta que ajuda a segui-lo |
| Colocar verbos na rota (`/criarGrupo`) | É o jeito mais natural de pensar | Use substantivos no plural e deixe a ação para o método HTTP |
| Esperar que o servidor "lembre" o pedido anterior | Em um aplicativo comum, a tela guarda o estado | Em REST, todo pedido leva tudo de que o servidor precisa |

## // Prática guiada

1. Pense em um sistema que você conhece (uma biblioteca, uma loja, um aplicativo de receitas) e liste três recursos dele, sempre no plural.
2. Para cada recurso, escreva a rota da coleção e a rota de um item específico.
3. Escreva, em JSON, um exemplo de um item de um desses recursos, com pelo menos quatro campos de tipos diferentes (texto, número, `true` ou `false`, e `null`).

## // Pratique sozinho

> **DESAFIO**
> Reescreva estas rotas no padrão REST: `/buscarMateria?id=2`, `/atualizarGrupo`, `/removerGrupo?id=5`. Para cada uma, diga também qual seria o método HTTP mais adequado, mesmo sem saber ainda todos eles (o Módulo 03 confere o seu palpite).

## // Aplicando no projeto da semana

1. Crie uma pasta chamada `api-grupos` no seu computador. Ela vai guardar todo o projeto da semana.
2. Dentro dela, crie um arquivo `README.md` com duas seções: "O que é o projeto" (uma frase) e "Rotas planejadas" (a tabela desta seção).
3. Se você versiona o projeto com Git, faça um commit: `git commit -m "Planeja as rotas da API"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Um tutorial que você encontrou na internet propõe criar a rota `/grupos/criar` para cadastrar um grupo. Que problema esse desenho traz, e como o padrão REST resolve?

Resposta: o problema é que o verbo "criar" está dentro do endereço. Para apagar, atualizar ou buscar, seria preciso inventar `/grupos/apagar`, `/grupos/atualizar` e assim por diante, e cada pessoa escolheria um nome diferente. No padrão REST, o endereço identifica só o recurso (`/grupos`), e a ação é dada pelo método: `POST /grupos` cria, `GET /grupos` lista, `DELETE /grupos/3` apaga.

## // Resumo do módulo

- [ ] Sei explicar o que é uma API e quais são os papéis de cliente e servidor.
- [ ] Sei o que é um recurso e como ele ganha um endereço.
- [ ] Sei ler e escrever um objeto simples em JSON.
- [ ] Sei as quatro ideias do estilo REST.
- [ ] Sei por que as rotas usam substantivos no plural, e não verbos.

---

**Próximo módulo:** `02-http-na-pratica.md`, a conversa entre cliente e servidor acontece por um protocolo chamado HTTP. Hora de ver como ele é por dentro.

`Material de Estudo // Coffee & Code`
