# atm_machines

A FastAPI uvicorn app that allows to create an atm and
then retrieve atms in specific location via filters.

## Running app locally

Start the app by running:

`docker-compose up atm_machines_local`

Apply migrations via:

`docker-compose run atm_machines_local alembic upgrade head`

`wait-for-it.sh` is one of the corners cut (see below).
If you see errors about `postgres` not being available,
wait a moment and restart the `atm_machines_local`.

Access the API via calls to `http://localhost:8000/`.

Openapi.json is accessible at `http://localhost:8000/openapi.json`.

Alternatively open `http://localhost:8000/docs` in browser for
interactive docs and demo of endpoints.

## Structure

The project is split into "apps" subfolders, simirlarly to [Django apps](https://docs.djangoproject.com/en/4.1/ref/applications/)
each containing own endpoints, controllers, schemas, models.

Generic code which is helpful to the whole web-server is found in [atm_machines](./atm_machines) root.
As well as the unit tests folder.

The only "domain" is [atms](./atm_machines/atms).

It describes 2 [endpoints](./atm_machines/atms/endpoints.py): `read_atms` and `create_atm`.

The code powering endpoints is stored in [AtmsController](./atm_machines/atms/controllers.py) - querying db, filtering, etc.

[schemas](./atm_machines/atms/schemas.py) power both parsing the user input and serializing output.

[models](./atm_machines/atms/models.py) describe tables in the db.

The unit tests are split by the endpoints and focus on testing controller logic as well as the views itself.

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

*why: formatting code manually is a pain; arguing about PEP8 compliance in PR reviews loses time*

Pytest for unit tests.

*why: familiarity; amount of features and plugins*

Dockerfile and docker-compose services for both local and remote usage.
Db as a volume for local app.

*why: to be able to launch the app with 1 command with expectation to
close-to-identical environment no matter what*

Db as indicated in Dockerfile - Postgresql+Postgis. Queried via Sqlalchemy+Geoalchemy2.
Adapter - psycopg2.

*why postgres: familiarity; ACID; plugins and docs*

*why psycopg2: familiarity; asyncpg fails to install and would've taken a lot of time to investigate*

*why sqlalchemy: popularity and familiarity*

Alembic for schema migrations

*why: popularity and familiarity*

Due to postgres adapter the Fastapi views are sync.

*why fastapi: fast in [benchmarks](http://klen.github.io/py-frameworks-bench/);
stable, feature-rich and popular in the community; concise*

Postgis is taken advantage of to query in the radius of location,
and return distance from the location.

Package versions are locked via pip-tools.

Request query parameters and body are parsed/validated by Pydantic.
The same for response.

Api is versioned via path.

*why: easier to explore; human readable and less prone to client errors; easier to support multiple versions*

Repo has the CI setup for building the image and running tests via Github Actions.

*why ci: mainly to flag non-working code ASAP and not let it even go to the review stage in that state*

*why Actions: code is hosted on Github and Actions are native*

# Cut corners

- error formatting (400, 500)
- error reporting via Sentry (var in settings is present)
- json formatting of logs
- Postgis indexes for geographies
- store lat/long separately from geography?
- automatic application of migrations
- model factories for tests
- more detailed unit tests
- load tests for endpoints (i.e. Artillery)
- pre-commit checks in CI
- endpoints for other CRUD operations
- wait for db to start
- better example data for request schemas in openapi.json

Deployment has been cut due to the timeframe,
however in case of more time and existence of a Kubernetes cluster,
following steps would've been taken:

- setup CD: push the built image to the registry
- write a helm chart for the app
  - Have all the DB-related things passed from the chart as env vars and ideally managed as secrets
  - start at least 2 pods to achieve relative availability during rolling restarts
- for the sake of the exersice, deploy behind basic-auth, but in real world - behind API gateway

A "cheap" version of it could be achieved via RDS and EC2 in AWS. Pull the image, start it behind nginx.

# Ideas for long term

- have tracing id in the logs
- health and readiness probes
- collect metrics (Premetheus?) about the deployment
- dashboards with metrics (p9x, memory, cpu, error rates...)
