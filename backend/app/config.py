"""
Central config for PrepGPT backend. Loads from .env using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"

    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "interview_prep"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Comma-separated list, e.g. "http://localhost:5173,https://prepgpt.vercel.app"
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


# Import this singleton everywhere instead of re-reading env vars
settings = Settings()