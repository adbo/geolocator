from sqlmodel import create_engine, Session, SQLModel
from core.config import Settings


settings = Settings()
engine = create_engine(settings.database_url)


def get_db():
    """Provides a database session."""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Creates database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
