Identificador de grupo - Parâmetro de Caminho
ex: "/grupos/{grupo\_id}"

* Com os grupos sendo um recurso mais concreto e o principal da API, faz sentido acessá-lo através do caminho diretamente



Termo de busca - Parâmetro de Consulta
ex: "/grupos?q=nomedogrupo"

* Visto que os termos de busca serão valores temporários inseridos pelo usuário, seria melhor deixá-los como valores de query para a leitura por GET



Filtro por matéria - Parâmetro de Caminho
ex: "/grupos/{materia\_id}"

* Poderia encaixar como os dois caminhos, porém acredito que por caminho seja melhor pois pode recarregar a página para mostrar uma lista incluindo somente os grupos com a matéria desejada mais facilmente



//=====================================================================

GET /materias



"/materias": {

&#x20;     "get": {

&#x20;       "summary": "Mostra uma lista completa com todas as matérias",

&#x20;       "operationId": "listar\_materias\_materias\_get",

&#x20;       "responses": {

&#x20;         "200": {

&#x20;           "description": "Successful Response",

&#x20;           "content": {

&#x20;             "application/json": {

&#x20;               "schema": {

&#x20;                 "items": {

&#x20;                   "$ref": "#/components/schemas/MateriaOut"

&#x20;                 },

&#x20;                 "type": "array",

&#x20;                 "title": "Response Listar Materias Materias Get"

&#x20;               }

&#x20;             }

&#x20;           }

&#x20;         }

&#x20;       }

&#x20;     }



Explicação: A tag GET foi gerada com base na rota, o summary e responses foram manualmente inseridas e acompanham a função e suas respectivas respostas



//=====================================================================

Instruções:

* Confira se a versão de FastAPI bate com o informado em requirements.txt (>=0.143,<0.144)
* Certifique-se que main.py, dados.py e schema.py estejam na mesma pasta
* Rode no ambiente virtual livremente



//=====================================================================

O que a API faz: A API é capaz de realizar um CRUD básico da lista grupos, além de fazer a leitura da lista matérias. 





























































