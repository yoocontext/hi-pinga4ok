# Luna Agent Template

Lightweight Python 3.14 application scaffold with four flat layers, dependency
injection, Docker Compose infrastructure, local `AGENTS.md` guides, and
pre-commit quality checks.

## Start a project

1. Create a repository with **Use this template**.
2. Replace `project-name` (slugs, images, services) and `project_name`
   (Python/database identifiers) with the real project name.
3. Install dependencies and hooks:

   ```bash
   uv sync --all-groups
   uv run pre-commit install
   ```

4. Create `.dev.env`:

   ```dotenv
   APP_PORT=8003

   PG__PORT=5432
   PG__DB=project_name
   PG__USER=project_name
   PG__PASSWORD=change-me
   PGADMIN_EMAIL=admin@example.com
   PGADMIN_PASSWORD=change-me
   PGADMIN_PORT=5050
   ```

5. Add the project-specific `Dockerfile` before running the app container.

## Commands

```bash
just pg                            # start Postgres
just pg-down                       # stop Postgres
just run                           # run the app locally with reload
just app                           # build/start the app container

uv run pre-commit run --all-files  # Ruff, pyright
uv run pytest                      # tests
```

## Architecture

| Layer | Responsibility | May depend on |
| --- | --- | --- |
| `bootstrap` | application assembly and IoC | all layers |
| `delivery` | controllers, schemas, validation, auth | `application` |
| `application` | use cases and contracts | its own pure code |
| `infra` | external implementations | application contracts |

Keep dependencies registered in `src/bootstrap/ioc/`. Do not instantiate them
outside IoC. See `AGENTS.md` for the full rules.
