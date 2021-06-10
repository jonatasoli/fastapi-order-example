# Definitions

- ext stay the general configs (database, base declarative model, broker connection e etc...)
- api.adapters stays externals communications
- api.endpoints stay the rotes
- services stay the business rules
- dao stay the queries
- models stay the database models
- schemas stay of pydantic schemas
- tests stay all tests in pytest
- locust stay locust test
- settings.toml and local.settings.toml is enviroments management with dynaconf

# Development

## Init project
- The project can be initialized with docker and python-poetry
- To add new libs need add with python-poetry to create deterministic version of lib
- Docker only install requirements.txt, so always to add new lib, run export requirements with python-poetry
```
poetry export -f requirements.txt --output requirements.txt
# with develop dependencies
poetry export -f requirements.txt --output requirements-dev.txt --dev --without-hashes
```

### Tests
- In toml file the envs run to docker, to run in python-poetry change envs in local.settings.toml above to localhost:
```
BASE_URL_PRODUCT = "http://localhost:8081"
BASE_URL_USER = "http://localhost:8082"
BROKER_SERVER = "localhost"
```
- In settings.toml
```
DB_DSN_MAIN = "postgresql+asyncpg://myuser:mypass@localhost:5432/orderdb"
```

### with python-poetry
- Run poetry install
```
poetry install
```
- Run poetry shell
```
poetry shell
```
- Run tests without docker-container and slow tests
```
cd app
pytest -s -m "not container slow"
```
- Run app
```
uvicorn --factory main:create_app --host 0.0.0.0 --port 8888 --reload
```
- Optional Run docker-compose file
```
docker-compose up -d
```

### with docker
- Run docker-compose file
```
docker-compose up -d
```
- Run requirements-dev
```
docker exec <service-order-container-name> bash -c "pip install -r requirements-dev.txt"
```

- Run tests
```
docker exec <service-order-container-name> bash -c "pytest -s"
```

## Start the app
- Run Command inside app file (container already started)
```
uvicorn --factory main:create_app --host 0.0.0.0 --port 8888 --reload
```

## Pre-Commit
To stay a clean code, we must install the pre-commit hook. Execute the following steps in project:

```
$ chmod +x pre-commit.sh
```

```
$ ln -s ../../pre-commit.sh .git/hooks/pre-commit
```

## Locust

```
locust -f ./order/locust/locust_order_endpoints.py
```

