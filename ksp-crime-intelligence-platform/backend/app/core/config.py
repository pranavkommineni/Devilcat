"""
Centralized application configuration.
All env-driven settings are loaded once and cached (singleton via lru_cache),
so every module imports the same settings instance instead of re-parsing .env.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Catalyst
    catalyst_project_id: str = "your_catalyst_project_id"
    catalyst_environment: str = "Development"
    catalyst_zone: str = "IN"
    catalyst_credential_json_path: str = "./catalyst-credentials.json"

    # Auth
    jwt_secret_key: str = "change_this_to_a_long_random_value"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # App
    app_env: str = "development"
    app_name: str = "CrimeLens AI"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:5173"

    # AI / ML
    convokraft_api_key: str = ""
    convokraft_endpoint: str = ""
    quickml_endpoint: str = ""

    # Cache
    cache_default_ttl_seconds: int = 300

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
