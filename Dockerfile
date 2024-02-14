FROM python:3.9-slim-buster

ENV POETRY_VERSION=1.7

RUN pip install --upgrade pip &&\
    pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY . /code

RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-ansi

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 80