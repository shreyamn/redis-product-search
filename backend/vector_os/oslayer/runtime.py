from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimeProfile:
    project_root: Path
    package_root: Path
    deployment_env: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str | None
    write_concurrency: int
    data_location: str

    @property
    def api_prefix(self) -> str:
        return "/api/v1"

    @property
    def docs_url(self) -> str:
        return "/api/docs"

    @property
    def openapi_url(self) -> str:
        return "/api/openapi.json"

    @property
    def redis_url(self) -> str:
        auth_segment = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth_segment}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def frontend_build_dir(self) -> Path:
        local_frontend_build = self.project_root / "frontend" / "build"
        if local_frontend_build.exists():
            return local_frontend_build
        return self.package_root / "templates" / "build"

    @property
    def schema_dir(self) -> Path:
        return self.package_root / "db" / "schema"

    @property
    def data_dir(self) -> Path:
        candidate = Path(self.data_location)
        if candidate.is_absolute():
            return candidate
        return (self.package_root / candidate).resolve()


_DEF_RELATIVE_DATA_DIR = "../../data"


def runtime_profile() -> RuntimeProfile:
    package_root = Path(__file__).resolve().parent.parent
    project_root = package_root.parent.parent
    return RuntimeProfile(
        project_root=project_root,
        package_root=package_root,
        deployment_env=os.environ.get("DEPLOYMENT", "dev"),
        redis_host=os.environ.get("REDIS_HOST", "localhost"),
        redis_port=int(os.environ.get("REDIS_PORT", 6379)),
        redis_db=int(os.environ.get("REDIS_DB", 0)),
        redis_password=os.environ.get("REDIS_PASSWORD"),
        write_concurrency=int(os.environ.get("WRITE_CONCURRENCY", 150)),
        data_location=os.environ.get("DATA_LOCATION", _DEF_RELATIVE_DATA_DIR),
    )
