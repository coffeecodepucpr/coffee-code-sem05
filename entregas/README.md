# Entregas | Semana 05

Aqui ficam as entregas de quem fez a Semana 05. A lista com o projeto de cada pessoa está no [README principal](../README.md#entregas-da-turma).

## Como entregar

1. Faça um **fork** deste repositório (botão *Fork*, no canto superior direito).
2. No seu fork, crie a pasta `entregas/Nome Sobrenome/`, com o seu nome e sobrenome.
3. Coloque seus arquivos dentro dela, seguindo a estrutura abaixo.
4. Faça commit e push no seu fork.
5. Abra um **Pull Request** para este repositório e preencha o modelo que aparece.

Depois do merge, a sua entrega entra na tabela do README principal.

> **Prefere manter o projeto no seu próprio repositório?** Também vale. Mande o link no Discord ou [abra uma issue](../../../issues/new) aqui com o link da pasta da semana, e ele entra na tabela do mesmo jeito. Só capriche no `README.md`, como explicado abaixo, porque é ele que vai aparecer primeiro.

## Estrutura esperada

```text
entregas/Nome Sobrenome/
└── api-grupos/
    ├── main.py
    ├── dados.py
    ├── schemas.py
    ├── requirements.txt
    └── README.md
```

- Não envie a pasta `.venv`, arquivos `__pycache__` nem um arquivo `.env`. Um `.gitignore` com essas três linhas resolve.
- Nomes de arquivo em minúsculas, separados por hífen ou sublinhado e **com extensão**.
- Altere só arquivos dentro da sua pasta.

## O que o seu README precisa ter

O `README.md` da sua pasta é a capa do seu projeto. Quem abrir precisa entender, sem você explicar:

- **o nome do projeto** como título;
- **uma frase** dizendo o que a API faz;
- **como instalar** (`pip install -r requirements.txt`) e **como rodar** (`fastapi dev main.py`);
- **as rotas principais**, ou uma indicação de que elas estão documentadas em `/docs` (Swagger).

## Já entregou em outra semana?

Sem problema repetir o mesmo projeto. Só lembre que cada semana é uma pasta completa: envie a versão atualizada dele aqui também.
