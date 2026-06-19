from fastapi import FastAPI

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
