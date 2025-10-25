FROM python:3.12-slim

WORKDIR /usr/src/app

# Install build deps
RUN apt-get update && apt-get install -y build-essential gcc curl && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN python -m pip install --upgrade pip && pip install poetry

# Copy project metadata and install dependencies via poetry
COPY pyproject.toml poetry.lock* /usr/src/app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the project
COPY . /usr/src/app

CMD ["celery", "-A", "worker.celery", "worker", "--loglevel=info"]
