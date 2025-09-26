from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FASTAPI_",
        case_sensitive=False
    )

settings = Settings()