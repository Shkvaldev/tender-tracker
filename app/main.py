from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.api.routes import auth, tenders
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(auth.router)
app.include_router(tenders.router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
