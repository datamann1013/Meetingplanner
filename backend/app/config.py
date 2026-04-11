"""
Application settings loaded from environment variables / .env file.
All configuration is centralised here — never import os.environ directly elsewhere.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://meetingplanner:devpassword@localhost:5432/meetingplanner"

    # JWT
    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 168  # 7 days

    # File storage
    storage_type: str = "local"  # "local" or "s3"
    storage_path: str = "./uploads"

    # CORS
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    # Email
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@yourorchestra.com"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Seed script
    seed_admin_email: str = "admin@yourorchestra.com"
    seed_admin_username: str = "admin"
    seed_admin_password: str = "changeme123"


settings = Settings()
