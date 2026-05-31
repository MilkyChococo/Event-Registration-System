from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def _is_truthy(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class Settings:
    env: str
    mongo_uri: str
    mongo_db_name: str
    secret: str
    seed_demo: bool
    use_mock_db: bool

    @classmethod
    def from_env(cls) -> "Settings":
        _load_dotenv()
        return cls(
            env=os.getenv("APP_ENV", "development"),
            mongo_uri=os.getenv("APP_MONGO_URI", "mongodb://127.0.0.1:27017"),
            mongo_db_name=os.getenv("APP_MONGO_DB_NAME", "event_registration"),
            secret=os.getenv("APP_SECRET", "change-me-for-production"),
            seed_demo=_is_truthy(os.getenv("APP_SEED_DEMO"), default=True),
            use_mock_db=_is_truthy(os.getenv("APP_USE_MOCK_DB"), default=False),
        )
