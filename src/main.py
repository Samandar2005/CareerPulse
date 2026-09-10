import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.v1.router import router as api_router

app = FastAPI(
    title="CareerPulse API",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api",
)

# Loyihaning asosiy yo'li
BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")