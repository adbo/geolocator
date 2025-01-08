from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    ipstack_api_key: str