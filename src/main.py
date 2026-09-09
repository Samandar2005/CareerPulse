from fastapi import FastAPI

from src.api.v1.router import router as api_router

app = FastAPI(
    title="CareerPulse API",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api",
)