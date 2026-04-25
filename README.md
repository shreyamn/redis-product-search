# Redis Product Search

Redis Product Search is a full-stack semantic search application for browsing and discovering retail products. It combines a FastAPI backend, a React frontend, and Redis vector search to support category filtering, image similarity search, and text-based product recommendations.

## Features

- Product catalog browsing with pagination
- Filters for gender and product category
- Image-based similarity search using stored image embeddings
- Text-based similarity search using product text embeddings
- Redis-backed vector index for fast nearest-neighbor lookup
- FastAPI service with interactive API documentation
- React single-page frontend for local exploration

## Tech Stack

- Backend: FastAPI, Python, RedisVL
- Frontend: React, TypeScript, Material UI
- Database: Redis with vector search support
- Tooling: Poetry, Docker Compose, npm

## Project Structure

```text
.
|-- backend/
|   |-- vector_os/
|   |   |-- api/
|   |   |-- db/
|   |   |-- oslayer/
|   |   |-- services/
|   |   `-- tests/
|   |-- pyproject.toml
|   `-- poetry.lock
|-- frontend/
|   |-- public/
|   |-- src/
|   `-- package.json
|-- data/
|-- docker-local-redis.yml
`-- README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry
- Node.js and npm
- Docker Desktop, or another Redis Stack-compatible Redis instance

### 1. Start Redis

```bash
docker compose -f docker-local-redis.yml up -d
```

Redis is expected at `localhost:6379`.

### 2. Configure Environment

Create a local `.env` file from the template if needed:

```bash
cp .env.template .env
```

Default values are suitable for local Docker-based development.

### 3. Install and Load the Backend

```bash
cd backend
poetry install
poetry run load
poetry run start
```

Backend URL: [http://localhost:8888](http://localhost:8888)  
API docs: [http://localhost:8888/api/docs](http://localhost:8888/api/docs)

### 4. Run the Frontend

In a second terminal:

```bash
cd frontend
npm install
npm start
```

Frontend URL: [http://localhost:3000](http://localhost:3000)

## API

The frontend uses the catalog API under:

```text
/api/v1/catalog/
```

The API supports listing products, filtering catalog results, and retrieving similar products from image or text vectors.

## Data

The loader expects product data at:

```text
data/products.json
```

If the local dataset is not present, the loader downloads the seed dataset configured in the backend.

## Development Notes

- Runtime paths and environment defaults are centralized in `backend/vector_os/oslayer/runtime.py`.
- Catalog query behavior lives in `backend/vector_os/services/catalog_service.py`.
- Redis index schema is defined in `backend/vector_os/db/schema/products.yml`.
- Generated logs, local environment files, build output, and dependency folders are intentionally ignored.
