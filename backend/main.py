"""FastAPI entrypoint.

Run:  uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from database import close_db, connect_db
from routes import chat as chat_routes
from routes import document as document_routes
from services.neo4j_service import close_driver as neo4j_close
from services.qdrant_service import init_collection as qdrant_init

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("legalsaathi")

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    try:
        qdrant_init()
    except Exception as e:
        log.warning("Qdrant init skipped: %r", e)
    yield
    await close_db()
    try:
        await neo4j_close()
    except Exception:
        pass


app = FastAPI(title="LegalSaathi AI", version="6.0.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    log.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    log.info("→ %s", response.status_code)
    return response


# Serve locally-uploaded PDFs when AWS is not configured.
_uploads_dir = Path(__file__).resolve().parent / "uploads"
_uploads_dir.mkdir(exist_ok=True)
app.mount("/local-files", StaticFiles(directory=_uploads_dir), name="local-files")

app.include_router(document_routes.router, prefix="/api/documents", tags=["documents"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["chat"])


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "6.0.0",
        "dev_mode": settings.DEV_MODE,
    }
