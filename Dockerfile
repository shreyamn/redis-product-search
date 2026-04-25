FROM node:22.0-alpine AS react_image

WORKDIR /app/frontend

ENV NODE_PATH=/app/frontend/node_modules
ENV PATH=$PATH:/app/frontend/node_modules/.bin

COPY ./frontend/package.json ./frontend/package-lock.json ./
RUN npm ci

ADD ./frontend ./
RUN npm run build

FROM python:3.11-slim-bookworm AS api_image

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/
VOLUME [ "/data" ]

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir -p /app/backend

COPY ./backend/poetry.lock ./backend/pyproject.toml ./backend/

WORKDIR /app/backend
RUN poetry install --all-extras --no-interaction

COPY ./backend/ .
COPY --from=react_image /app/frontend/build /app/backend/vector_os/templates/build

CMD ["poetry", "run", "start-app"]
