from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class GlobalSettings(BaseSettings):
    ENV_NAME: str = "dev"

    SENTRY_DSN: Optional[str]

    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: Optional[str]
    DB_PORT: Optional[str]
    DB_NAME: str = "atm_machines"
    DB_URI: Optional[PostgresDsn] = None

    @validator("DB_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USERNAME"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT", ""),
            path=f'/{values.get("DB_NAME", "")}',
        )


settings = GlobalSettings()
