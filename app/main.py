"""
RSSify main FastAPI application entrypoint.
"""
from fastapi import FastAPI

from app.routers import sites, feeds
from app.scheduler import TaskScheduler, schedule_individual_site_checks
from app.database import SessionLocal
from app.scraper import WebScraper

app = FastAPI()
app.include_router(sites.router)
app.include_router(feeds.router)

scheduler = TaskScheduler()

@app.on_event("startup")
def start_scheduler():
    scheduler.start()
    # Индивидуальные задачи для каждого сайта с учетом check_interval
    schedule_individual_site_checks(scheduler, SessionLocal, WebScraper())

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/health", tags=["admin"])
def healthcheck():
    """
    Healthcheck endpoint для проверки статуса сервиса.
    """
    return {"status": "ok"}
