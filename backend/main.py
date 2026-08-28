from fastapi import FastAPI

from backend.api.routes import router

from backend.database.database import (
    Base,
    engine
)

from backend.database import models


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="AI Sports Coach",
    description=(
        "AI-powered sports talent assessment "
        "and performance improvement system"
    ),
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Sports Coach Backend is running!",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(
    router,
    prefix="/api"
)