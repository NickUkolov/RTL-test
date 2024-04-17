from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    COLLECTION_NAME: str

    TG_TOKEN: str


settings = Settings(_env_file=".env.test", _env_file_encoding="utf-8")
