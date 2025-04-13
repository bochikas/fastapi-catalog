# API Каталог товаров

---

## Стек технологий

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Poetry
- Pydantic

---

## Установка и запуск (Linux)

### 1. Клонируй репозиторий

```bash
git clone https://github.com/bochikas/fastapi-catalog.git
cd fastapi-catalog
```

### 2. Установи зависимости
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip poetry
poetry install --without dev
```

### 3. Создай .env файл
```
POSTGRES_NAME=db_name
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

### 4. Применение миграций
```bash
alembic upgrade head
```

### 5. Запуск сервера
```bash
poetry run uvicorn main:app
```

После запуска, API будет доступно по адресу http://127.0.0.1:8000

Документация Swagger доступна по адресу http://127.0.0.1:8000/docs
