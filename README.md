# Heart Disease Prediction

Este projeto é uma aplicação Flask que utiliza várias bibliotecas e frameworks para realizar diversas tarefas. O projeto
está escrito em Python 3.10.11.

## Objetivo

O objetivo é classificar os pacientes em duas categorias  
1. O paciente pode portar/desenvolver doença cardiaca.
2. Não há indícios de que o paciente tenha/possa ter doença cardiaca.
3. Os dados inputados são persistidos em uma base de dados SQLite.

## Bibliotecas utilizadas

- **Flask**: Um micro framework para a criação de aplicações web.
- **SQLAlchemy**: ORM (Object Relational Mapper) para interagir com bancos de dados.
- **IPython**: Ambiente interativo de Python.
- **Matplotlib**: Biblioteca para criação de gráficos.
- **NumPy**: Biblioteca para computação numérica.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Pillow**: Biblioteca para processamento de imagens.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **Scikit-learn**: Biblioteca para machine learning.

## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/jbrunomf/mvp-sistemas-inteligentes-pucrj
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd seu-repositorio
    ```

3. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate  # Para Windows
    ```

4. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para iniciar a aplicação Flask, execute o seguinte comando no terminal:

```bash
flask run
```

A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Estrutura do Projeto