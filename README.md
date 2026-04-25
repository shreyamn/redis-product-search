# Vector OS

Vector OS is a local-first catalog exploration project built for running on your own machine. It keeps the original strengths of the repository, including vector similarity search by image and by text, but reshapes the project into a more structured FastAPI + React application with an explicit OS abstraction layer.

## What changed

- Renamed the project identity to `Vector OS`
- Reorganized the backend package from `productsearch` to `vector_os`
- Added `backend/vector_os/oslayer/runtime.py` as the operating-system abstraction layer for environment values, file paths, build paths, schema paths, and runtime defaults
- Split catalog logic into a service layer in `backend/vector_os/services/catalog_service.py`
- Renamed the public API route from `/api/v1/product` to `/api/v1/catalog`
- Updated the frontend copy and styling to match the new project identity
- Kept the core functionality: list items, filter by category/gender, find similar items by image, and find similar items by text

## Project structure

```text
/backend
  /vector_os
    /api
    /db
    /oslayer
    /services
    /tests
    main.py
/frontend
  /src
  /public
/data
```

## Local run

### 1. Start Redis locally

You need a Redis instance with vector search support running on `localhost:6379`.

If you already have Docker installed, the simplest option is:

```bash
docker compose -f docker-local-redis.yml up
```

### 2. Run the backend

```bash
cd backend
poetry install
poetry run load
poetry run start
```

Backend URL: [http://localhost:8888](http://localhost:8888)
API docs: [http://localhost:8888/api/docs](http://localhost:8888/api/docs)

### 3. Run the frontend

```bash
cd frontend
npm install
npm start
```

Frontend URL: [http://localhost:3000](http://localhost:3000)

## Core features

- Catalog browsing with pagination
- Filtering by gender and category
- Image-based similarity lookup
- Text-vector similarity lookup
- Single-page frontend served by React
- FastAPI backend ready for local development

## Notes

- The backend expects the dataset at `data/products.json`. If that file is missing, the loader falls back to the remote seed source.
- The UI talks to the backend through `/api/v1/catalog/`.
- The OS abstraction layer lives in [backend/vector_os/oslayer/runtime.py](backend/vector_os/oslayer/runtime.py) and centralizes runtime-dependent paths and environment defaults.
