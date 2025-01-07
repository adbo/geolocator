from sqlmodel import create_engine, Session
from core.config import Settings

settings = Settings()

engine = create_engine(settings.database_url)

def get_db():
    with Session(engine) as session:
        yield session