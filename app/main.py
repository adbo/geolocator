from fastapi import FastAPI

from api.endpoints import router as api_router
from db.database import create_db_and_tables


app = FastAPI(on_startup=[create_db_and_tables])

app.include_router(api_router, prefix="/api/v1")

def on_startup():
    create_db_and_tables()