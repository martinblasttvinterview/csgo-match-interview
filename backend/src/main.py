
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router


def get_app() -> FastAPI:
    """Get FastAPI app."""
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=["*"])
    app.include_router(router, prefix="/api")
    return app
