set dotenv-load := true

compose := "docker compose --env-file .dev.env"

app:
    {{compose}} -f docker_compose/app.yaml up -d --build

app-down:
    {{compose}} -f docker_compose/app.yaml down

pg:
    {{compose}} -f docker_compose/pg.yaml up -d

pg-down:
    {{compose}} -f docker_compose/pg.yaml down

run:
    uv run uvicorn bootstrap.app:create_app --factory --app-dir src --reload --port ${APP_PORT}

migrate:
    uv run alembic upgrade head

migration name:
    uv run alembic revision --autogenerate -m "{{name}}"
