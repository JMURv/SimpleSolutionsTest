FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ./app

COPY ./poetry.lock ./pyproject.toml ./

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . ./
