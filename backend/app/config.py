"""
Central config for PrepGPT backend. Loads from .env using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"

    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "interview_prep"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Import this singleton everywhere instead of re-reading env vars
settings = Settings()