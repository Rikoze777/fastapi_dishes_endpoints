FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock .

RUN pip3 install poetry

RUN poetry install

EXPOSE 8000

COPY . .

ENTRYPOINT ["poetry", "run"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]