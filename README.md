# Case Opener

Learning project on clean architecture: players open cases, collect items,
and gift them to each other.

## Run

1. Install dependencies and hooks:

   ```bash
   uv sync --all-groups
   uv run pre-commit install
   ```

2. Create `.dev.env`:

   ```dotenv
   APP_PORT=8003

   PG__PORT=5432
   PG__DB=case_opener
   PG__USER=case_opener
   PG__PASSWORD=change-me
   PG__ECHO=false
   PGADMIN_EMAIL=admin@example.com
   PGADMIN_PASSWORD=change-me
   PGADMIN_PORT=5050

   PLAYERS__START_BALANCE=500
   PLAYERS__DAILY_BONUS=100
   PLAYERS__DAILY_BONUS_COOLDOWN=PT24H
   ```

   `PG__ECHO=true` prints every SQL query the app sends.

3. Start Postgres, apply migrations, run the app:

   ```bash
   just pg
   just migrate
   just run
   ```

   Migrations create the schema and a catalog of two cases. API docs:
   `http://localhost:${APP_PORT}/docs`.

## API

Endpoints that act for a player read their id from the `X-Player-Id` header.

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/v1/players` | create a player |
| `GET` | `/api/v1/players/{player_id}` | get a player |
| `POST` | `/api/v1/players/me/daily-bonus` | claim the daily bonus |
| `GET` | `/api/v1/cases` | list cases with drop chances |
| `POST` | `/api/v1/cases/{case_id}/open` | open a case |
| `GET` | `/api/v1/players/{player_id}/inventory` | list a player's items |
| `POST` | `/api/v1/inventory/{inventory_item_id}/gift` | gift an item |
| `GET` | `/api/v1/leaderboard` | players with the most items |

## Commands

```bash
just pg                            # start Postgres
just pg-down                       # stop Postgres
just migrate                       # apply migrations
just migration "name"              # autogenerate a migration
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
