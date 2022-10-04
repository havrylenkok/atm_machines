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

Alternatively open `http://localhost:8000/docs` in browser for
interactive docs and demo of endpoints.

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

# Notable

The app has pre-commit checks set up: black, isort, mypy...

Pytest for unit tests.

Dockerfile and docker-compose services for both local and remote usage.
Db as a volume for local app.

Db as indicated in Dockerfile - Postgis. Queried via Sqlalchemy+Geoalchemy2.
Adapter - psycopg2. Mainly because with asyncpg fails to install and would've taken
a lot of time to investigate.

Alembic for schema migrations.

Due to postgres adapter the Fastapi views are sync.

Postgis is taken advantage of to query in the radius of location,
and return distance from the location.

Package versions are locked via pip-tools.

Request query parameters and body are parsed/validated by Pydantic.
The same for response.

Api is versioned via path.

Repo has the CI setup for building the image and running tests via Github Actions.

# Cut corners

- error formatting (400, 500)
- json formatting of logs
- Postgis indexes for geographies
- better pydantic schemas for create response
  - store lat/long separately from geography
- automatic application of migrations
- model factories for tests
- more detailed unit tests
- load tests for endpoints (i.e. Artillery)
- pre-commit checks in CI

Deployment has been cut due to the timeframe,
however in case of more time and existence of a Kubernetes cluster,
following steps would've been taken:

- setup CD: push the built image to the registry
- write a helm chart for the app
  - Have all the DB-related things passed from the chart as env vars and ideally managed as secrets
  - start at least 2 pods to achieve relative availability during rolling restarts
- for the sake of the exersice, deploy behind basic-auth, but in real world - behind API gateway
  - I've used Kong

A "cheap" version of it could be achieved via RDS and EC2 in AWS. Pull the image, start it behind nginx.

# Ideas for long term

- have tracing id in the logs
- health and readiness probes
- collect metrics (Premetheus?) about the deployment
-
