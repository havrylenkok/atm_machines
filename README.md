# atm_machines

A FastAPI uvicorn app that allows to create an atm and
then retrieve atms in specific location via filters.

## Running app locally

Start the app by running:

`docker-compose up atm_machines_local`

Apply migrations via:

`docker-compose run atm_machines_local alembic upgrade head`

Access the API via calls to `http://localhost:8000/`.

Openapi.json is accessible at `http://localhost:8000/openapi.json`.

Alternatively open `http://localhost:8000/docs` in browser for interactive docs and demo of endpoints.

## Update dependencies

```bash
docker-compose run atm_machines_local bash

> pip install pip-tools
> pip-compile requirements/base.in
> exit
```

Commit the changed files.

## Running tests

```bash
docker-compose up --build atm_machines_tests
```

## Guidelines

Take advantage of pre-commit hooks via

```bash
pip install pre-commit

pre-commit install
```

# Todo
- Push to github, setup CI
- Deploy with EC2?

# Cut corners

- error formatting (400, 500)
- logs and json formatting
- Postgis indexes for geographies
- better pydantic schemas for create response
  - store lat/long separately from geography
- manual application of migrations
- model factories for tests
- detailed unit tests
- load tests for endpoints
