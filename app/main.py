"""
RSSify main FastAPI application entrypoint.
"""
from fastapi import FastAPI

from app.routers import sites, feeds

app = FastAPI()
app.include_router(sites.router)
app.include_router(feeds.router)

@app.get("/health", tags=["admin"])
def healthcheck():
    """
    Healthcheck endpoint для проверки статуса сервиса.
    """
    return {"status": "ok"}
