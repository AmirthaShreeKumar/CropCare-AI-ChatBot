from __future__ import annotations
from typing import Optional
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    google_api_key: str
    groq_api_key: str
    app_secret: str

    database_url: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None

    max_image_upload_mb: int = 6
    max_audio_upload_mb: int = 10
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        missing = [
            name
            for name in ("db_user", "db_password", "db_host", "db_port", "db_name")
            if getattr(self, name) is None
        ]
        if missing:
            raise ValueError(
                "DATABASE_URL or all DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME must be set. "
                f"Missing: {', '.join(missing)}"
            )

        return (
            f"postgresql://{self.db_user}:{quote_plus(self.db_password)}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = AppSettings()
# eager validation of DB URL and secrets
_ = settings.resolved_database_url
