## Star Wars API

Projeto desenvolvido como desafio utilizando Python e Flask, hospedado no Google Cloud Functions. A API consome dados da SWAPI
e permite buscas, filtros e paginação.


---

## Funcionalidades

- Endpoint de **health check**
- Busca por diferentes recursos da API Star Wars (`people`, `planets`, `films`, `species`, `vehicles`, `starships`)
- Filtros por campos específicos
- Paginação
- Listagem de personagens de filmes específicos
- Documentação via OpenAPI (para integração com API Gateway)

---

## Tecnologias

- Python 3.11
- Flask 2.3
- Requests
- Google Cloud Functions (GCP)

---

## Estrutura do Projeto

starwars-api/
│
├── app/
│ ├── routes.py
│ ├── services/
│ │ └── swapi_service.py
│ └── utils/
│ ├── errors.py
│ ├── filters.py
│ ├── sort.py
│ └── validators.py
│
├── main.py
├── requirements.txt
└── openapi.yaml

## Configuração e execução local

## Crie e ative um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


## Instale as dependências:

pip install -r requirements.txt


## Execute a API localmente:

export FLASK_APP=main.py
export FLASK_ENV=development
flask run

