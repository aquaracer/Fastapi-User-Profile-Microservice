FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root


COPY . /app


CMD ["poetry","run","uvicorn", "main:app", "--host", "0.0.0.0","--port","8080","--reload"]