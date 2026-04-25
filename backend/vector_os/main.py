from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from vector_os import config
from vector_os.api.main import api_router
from vector_os.db.utils import get_async_index
from vector_os.oslayer import runtime_profile
from vector_os.spa import SinglePageApplication

runtime = runtime_profile()


@asynccontextmanager
async def lifespan(app: FastAPI):
    index = await get_async_index()
    async with index:
        yield


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=config.API_V1_STR)
app.mount("/data", StaticFiles(directory=str(runtime.data_dir)), name="data")
app.mount(path="/", app=SinglePageApplication(directory=runtime.frontend_build_dir), name="SPA")


def main():
    server_options = {"host": "0.0.0.0", "reload": True, "port": 8888, "workers": 1}
    if config.DEPLOYMENT_ENV == "prod":
        server_options.update(
            {
                "reload": False,
                "workers": 2,
                "ssl_keyfile": "key.pem",
                "ssl_certfile": "full.pem",
            }
        )

    uvicorn.run("vector_os.main:app", **server_options)


if __name__ == "__main__":
    main()
