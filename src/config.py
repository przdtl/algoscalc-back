from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_url(self):
        return 'redis://redis_db:6379/0'

    # model_config = SettingsConfigDict(
    #     # `.env.prod` takes priority over `.env`
    #     env_file=('.env.prod', '.env'),
    #     env_file_encoding='utf-8'
    # )
    class Config:
        env_file = ".env"
        extra = "allow"  # this allows all the other env vars


settings = Settings()
