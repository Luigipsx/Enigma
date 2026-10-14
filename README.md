
# AV5 - Sistema de Enigmas

Sistema desenvolvido em Python para gerenciamento de enigmas e tentativas, utilizando SQLAlchemy e oferecendo suporte aos bancos de dados SQLite e MySQL.

O sistema permite cadastrar, listar e excluir enigmas e tentativas, verificar respostas informadas e alternar entre os bancos de dados durante a execução.

## Tecnologias utilizadas

- Python
- SQLAlchemy
- SQLite
- MySQL
- PyMySQL
- python-dotenv
- uv

## Modelagem do sistema

O sistema possui duas classes principais relacionadas por meio de uma associação de um para muitos (1:N).

### Classe Enigma

| Atributo | Tipo | Descrição |
|---|---|---|
| id | Inteiro | Identificador único do enigma |
| titulo | String | Título do enigma |
| descricao | String | Descrição do enigma |
| resposta | String | Resposta correta do enigma |
| limite_tentativas | Inteiro | Número máximo de tentativas |
| resolvido | Booleano | Indica se o enigma foi resolvido |

### Classe Tentativa

| Atributo | Tipo | Descrição |
|---|---|---|
| id | Inteiro | Identificador único da tentativa |
| enigma_id | Inteiro | Chave estrangeira que referencia o enigma |
| resposta_informada | String | Resposta informada pelo usuário |
| numero_tentativa | Inteiro | Número da tentativa realizada |
| resultado | String | Resultado: acertou ou errou |

### Relacionamento entre as classes

Um enigma pode possuir várias tentativas, enquanto cada tentativa pertence a um único enigma.

O atributo `enigma_id` da classe `Tentativa` é uma chave estrangeira que referencia o atributo `id` da classe `Enigma`.

## Pré-requisitos

Para executar o projeto, é necessário ter instalado:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

O MySQL é necessário somente se você optar por utilizar esse banco de dados. O SQLite não exige a instalação de um servidor.

## Como baixar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/Luigipsx/Enigma
```

Entre na pasta do projeto:

```bash
cd Enigma
```

Caso a pasta tenha outro nome, utilize o nome correspondente.

## Instalação das dependências

Na raiz do projeto, execute:

```bash
uv sync
```

Esse comando instala as dependências e prepara o ambiente virtual do projeto.

## Como executar o programa

Execute o seguinte comando:

```bash
uv run python -m src.enigma.main
```

O programa será iniciado no terminal e apresentará um menu interativo.

## Funcionalidades

O sistema possui as seguintes opções:

```text
1 - Inserir enigma
2 - Listar enigmas
3 - Excluir enigma
4 - Inserir tentativa
5 - Listar tentativas
6 - Excluir tentativa
7 - Alterar banco de dados
0 - Sair
```

### Operações com enigmas

- Cadastrar enigmas informando título, descrição, resposta correta e limite de tentativas.
- Listar os enigmas cadastrados.
- Excluir enigmas.

O atributo `resolvido` começa com o valor `False` e passa para `True` quando o enigma é respondido corretamente.

### Operações com tentativas

- Registrar uma tentativa de resolução.
- Listar as tentativas cadastradas.
- Excluir tentativas.

Cada tentativa está vinculada a um enigma por meio do atributo `enigma_id`.

O sistema verifica se a resposta informada corresponde à resposta correta e registra o resultado como `acertou` ou `errou`. Também considera o limite de tentativas definido para cada enigma.

## Bancos de dados

O sistema inicia utilizando SQLite, mas também permite utilizar MySQL.

### SQLite

O arquivo do banco de dados é:

```text
enigmas.db
```

O banco é criado automaticamente pelo programa conforme a implementação do projeto. Não é necessária configuração adicional.

### MySQL

Para utilizar o MySQL, é necessário ter o servidor instalado e em execução.

O banco de dados utilizado é `luigi_av5`.

Crie o banco de dados:

```sql
CREATE DATABASE luigi_av5;
```

Na raiz do projeto, crie um arquivo chamado `.env` e adicione:

```env
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=luigi_av5
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

Substitua `sua_senha` pela senha do seu usuário MySQL.

## Alteração do banco de dados

Para alterar o banco de dados durante a execução:

1. Selecione a opção `7 - Alterar banco de dados`.
2. Escolha uma das opções disponíveis:

```text
1 - SQLite
2 - MySQL
```

Para utilizar o MySQL, verifique se o servidor está em execução, se o banco `luigi_av5` existe e se o arquivo `.env` está configurado corretamente.

## Estrutura do projeto

```text
Enigma/
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── uv.lock
└── src/
    └── enigma/
        ├── __init__.py
        ├── database.py
        ├── main.py
        └── models.py
```

O arquivo `.env` deve ser criado localmente quando necessário. O arquivo `enigmas.db` pode ser gerado durante a utilização do SQLite.

## Instalação e execução rápida

Depois de substituir a URL do repositório e confirmar o nome da pasta, execute:

```bash
git clone https://github.com/Luigipsx/Enigma
cd Enigma
uv sync
uv run python -m src.enigma.main
```

Para utilizar o MySQL:

1. Inicie o servidor MySQL.
2. Crie o banco de dados `luigi_av5`.
3. Configure o arquivo `.env`.
4. Execute o programa.