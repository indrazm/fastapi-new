from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    OPENAPI_URL: str = "/openapi.json"
    SCALAR_URL: str = "/scalar"

    class Config:
        env_file = ".env"
        extra = "ignore"
