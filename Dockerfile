FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock .

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]