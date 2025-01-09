from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from api.endpoints import router as api_router
from db.database import create_db_and_tables
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

async def on_startup():
    """Initializes the application on startup."""
    create_db_and_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application lifespan.

    Args:
        app: The FastAPI application instance.
    """
    await on_startup()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handles SQLAlchemy database exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Database error: {str(exc)}"},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handles general, unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An unexpected error occurred: {str(exc)}"},
    )

app.include_router(api_router, prefix="/api/v1")