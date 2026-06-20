from fastapi import FastAPI

from app.db.database import Base, engine

import app.models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DealLens API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "DealLens API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
