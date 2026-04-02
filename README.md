# API de Endereços (API Principal)

## 📌 Descrição

Esta API é responsável pelo gerenciamento de endereços a partir de CEPs, permitindo operações de CRUD (Create, Read, Update/Put e Delete), além de integração com serviços externos para enriquecimento dos dados.

A aplicação consome:

* ViaCEP → para obter dados do endereço
* Nominatim → para obter coordenadas geográficas de latitude e longitude
* API de Distância (secundária) → para cálculo de distância entre endereços

---

## 🧱 Arquitetura

A aplicação foi construída seguindo o padrão de microsserviços:

* API Principal: gerenciamento de endereços
* API Secundária: cálculo de distância

Comunicação entre APIs ocorre via HTTP.

---

## 🚀 Funcionalidades

* Criar endereço a partir de CEP
* Listar todos os endereços
* Buscar endereço por ID
* Filtrar endereços por estado
* Atualizar endereço (via novo CEP)
* Deletar endereço
* Calcular distância entre dois endereços

---

## 🔗 APIs Externas Utilizadas

* ViaCEP: https://viacep.com.br/
* Nominatim (OpenStreetMap): https://nominatim.openstreetmap.org/ui/search.html

---

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/downloads/)
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [Flask-OpenAPI3 (Swagger)](https://swagger.io/specification/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Docker](https://www.docker.com/products/docker-desktop/)

---

## Como configurar o Ambiente Virtual

Esse tópico explica de forma simples como criar e ativar o ambiente virtual [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Digite os seguintes códigos em ordem no terminal de comando:

- Caso o virtualenv ainda não esteja instalado
```
pip install virtualenv
```

- Criar o ambiente virtual dentro da pasta backend
```
python -m venv venv
```

- Ativar o ambiente virtual
```
venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/MacOS)
```

---

## Como executar a API Flask

Será necessário instalar todas as bibliotecas presentes no arquivo **requirements.txt**. Para isso, é necessário abrir o terminal pelo diretório raiz do projeto e executar o seguinte comando (já com o ambiente virtual ativado).

```
(venv)$ pip install -r requirements.txt
```

Para executar a API, digite no prompt:
```
(venv)$ flask run --host 0.0.0.0 --port 5000
```

Caso queira utilizar em modo de desenvolvimento (sempre que o código for mudado, o servidor será reiniciado), digite essa linha:
```
(venv)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Entre no http://localhost:5000/#/ no navegador para utilizar a API.

---

## 📦 Como executar (Docker)

### Pré-requisitos

* Docker Desktop instalado

### Passos

```bash
docker-compose up --build
```

---

## 🌐 Endpoints principais

### POST /endereco

Cria um novo endereço a partir de um CEP

### GET /enderecos

Lista todos os endereços

### GET /endereco?id=1

Busca um endereço específico

### PUT /endereco

Atualiza um endereço

### DELETE /endereco?id=1

Remove um endereço

### GET /enderecos/estado?estado=SP

Filtra endereços por estado

### GET /distancia?id1=1&id2=2

Calcula a distância entre dois endereços

---

## 📄 Documentação

A documentação da API pode ser acessada via Swagger:

```
http://localhost:5000/openapi
```

---

## 🧠 Decisões de Projeto

* Uso de CEP como entrada principal
* Uso de APIs externas para enriquecimento de dados
* Separação de responsabilidades em dois serviços
* Uso de Enum para estados (filtro e dropdown)
