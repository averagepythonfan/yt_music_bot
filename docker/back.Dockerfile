FROM python:3.10-slim

RUN pip install "poetry==1.3.2"

RUN apt-get update && apt-get install ffmpeg -y

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --only back --no-root

COPY src/ src/