"""
RSSify main FastAPI application entrypoint.
"""
from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.exc import IntegrityError

from app.routers import sites, feeds
from app.scheduler import TaskScheduler, schedule_individual_site_checks
from app.database import SessionLocal, get_db
from app.models import Site
from app.scraper import WebScraper

app = FastAPI()
app.include_router(sites.router)
app.include_router(feeds.router)

# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", tags=["web"])
def index(request: Request, db: Session = Depends(get_db)):
    """
    Корневая страница: список сайтов (web UI).
    """
    sites = db.query(Site).all()
    return templates.TemplateResponse("sites_list.html", {"request": request, "sites": sites})

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

@app.post("/add-site", tags=["web"])
def add_site(
    request: Request,
    name: str = Form(...),
    url: str = Form(...),
    selector: str = Form(...),
    title_selector: str = Form(None),
    desc_selector: str = Form(None),
    link_selector: str = Form(None),
    description: str = Form(None),
    is_active: str = Form(None),
    check_interval: int = Form(10),
    db: Session = Depends(get_db),
):
    """
    Обработчик формы добавления нового сайта.
    """
    site = Site(
        name=name.strip(),
        url=url.strip(),
        selector=selector.strip(),
        title_selector=title_selector.strip() if title_selector else None,
        desc_selector=desc_selector.strip() if desc_selector else None,
        link_selector=link_selector.strip() if link_selector else None,
        description=description.strip() if description else None,
        is_active=1 if is_active else 0,
        check_interval=check_interval or 10,
    )
    db.add(site)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Можно добавить flash-сообщение об ошибке (например, дублирующий URL)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
