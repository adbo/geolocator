from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the application."""

    database_url: str
    ipstack_api_key: str
