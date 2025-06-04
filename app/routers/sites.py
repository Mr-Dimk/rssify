"""
Sites API router for CRUD operations on Site model.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List
from fastapi import BackgroundTasks
from app.scraper import WebScraper

router = APIRouter(
    prefix="/api/sites",
    tags=["sites"]
)

# Dependency to get DB session
def get_db():
    db = database.get_db()
    try:
        yield from db
    finally:
        pass

@router.get("/", response_model=List[schemas.SiteWithPosts])
def list_sites(db: Session = Depends(database.get_db)):
    """
    Получить список всех сайтов с вложенными постами.
    """
    sites = db.query(models.Site).all()
    return sites

@router.get("/{site_id}", response_model=schemas.SiteWithPosts)
def get_site(site_id: int, db: Session = Depends(database.get_db)):
    """
    Получить конкретный сайт по ID с вложенными постами.
    """
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/", response_model=schemas.SiteWithPosts, status_code=status.HTTP_201_CREATED)
def create_site(site: schemas.SiteCreate, db: Session = Depends(database.get_db)):
    """
    Создать новый сайт для мониторинга.
    """
    # Проверка на уникальность URL
    existing = db.query(models.Site).filter(models.Site.url == site.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Site with this URL already exists")
    db_site = models.Site(
        name=site.name,
        url=str(site.url),
        selector=site.selector,
        description=site.description,
        is_active=1 if site.is_active else 0
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.put("/{site_id}", response_model=schemas.SiteWithPosts)
def update_site(site_id: int, site_update: schemas.SiteUpdate, db: Session = Depends(database.get_db)):
    """
    Обновить данные сайта по ID.
    """
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    # Проверка на уникальность URL, если обновляется url
    if site_update.url and site_update.url != site.url:
        existing = db.query(models.Site).filter(models.Site.url == str(site_update.url)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Site with this URL already exists")
        site.url = str(site_update.url)
    if site_update.name is not None:
        site.name = site_update.name
    if site_update.selector is not None:
        site.selector = site_update.selector
    if site_update.description is not None:
        site.description = site_update.description
    if site_update.is_active is not None:
        site.is_active = 1 if site_update.is_active else 0
    db.commit()
    db.refresh(site)
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(database.get_db)):
    """
    Удалить сайт по ID (каскадно удаляет посты).
    """
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    db.delete(site)
    db.commit()
    return None

@router.post("/{site_id}/check", status_code=200)
def check_site(site_id: int, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    """
    Принудительно запустить проверку сайта (асинхронно).
    """
    site = db.query(models.Site).filter(models.Site.id == site_id, models.Site.is_active == 1).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found or inactive")
    def do_check():
        scraper = WebScraper()
        try:
            soup = scraper.fetch_page(site.url)
            # Здесь можно добавить логику обновления постов и last_check
        except Exception as e:
            # Здесь можно добавить обработку ошибок и обновление last_error
            pass
    background_tasks.add_task(do_check)
    return {"detail": "Check started"}

@router.get("/api/stats", tags=["admin"])
def get_stats(db: Session = Depends(database.get_db)):
    """
    Получить статистику сервиса (количество сайтов, постов).
    """
    sites_count = db.query(models.Site).count()
    posts_count = db.query(models.Post).count()
    return {"sites": sites_count, "posts": posts_count}

@router.get("/api/logs", tags=["admin"])
def get_logs():
    """
    Получить последние строки из лог-файла (если есть).
    """
    import os
    log_path = os.path.join(os.getcwd(), "logs", "app.log")
    if not os.path.exists(log_path):
        return {"logs": "Log file not found"}
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-50:]
    return {"logs": "".join(lines)}
