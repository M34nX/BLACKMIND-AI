from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BLACKMIND-AI"
    model_base_url: str = "https://api.openai.com/v1"
    model_name: str = "replace-with-a-supported-model"
    model_api_key: str = ""
    model_timeout_seconds: float = 90.0
    model_max_tokens: int = 5000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
