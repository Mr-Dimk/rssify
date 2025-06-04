"""
Feeds API router for RSS and Atom endpoints.
"""
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app import models, database, rss_generator

router = APIRouter(
    tags=["feeds"]
)

@router.get("/feed/{site_id}", response_class=Response, tags=["feeds"])
def get_rss_feed(site_id: int, db: Session = Depends(database.get_db)):
    """
    Получить RSS фид для сайта по его ID.
    """
    site = db.query(models.Site).filter(models.Site.id == site_id, models.Site.is_active == 1).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found or inactive")
    posts = site.posts
    gen = rss_generator.RSSGenerator(
        title=site.name,
        link=site.url,
        description=site.description or site.name
    )
    for post in posts:
        gen.add_item(
            title=post.title,
            link=post.url,
            description=post.description,
            pubdate=post.published_at,
            guid=post.content_hash or post.url
        )
    xml = gen.generate_feed()
    return Response(content=xml, media_type="application/rss+xml; charset=utf-8")

@router.get("/feed/{site_id}/atom", response_class=Response, tags=["feeds"])
def get_atom_feed(site_id: int, db: Session = Depends(database.get_db)):
    """
    Получить Atom фид для сайта по его ID.
    """
    site = db.query(models.Site).filter(models.Site.id == site_id, models.Site.is_active == 1).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found or inactive")
    posts = site.posts
    gen = rss_generator.RSSGenerator(
        title=site.name,
        link=site.url,
        description=site.description or site.name
    )
    for post in posts:
        gen.add_item(
            title=post.title,
            link=post.url,
            description=post.description,
            pubdate=post.published_at,
            guid=post.content_hash or post.url
        )
    xml = gen.generate_atom_feed()
    return Response(content=xml, media_type="application/atom+xml; charset=utf-8")

# Обработка ошибок уже реализована: если сайт не найден или неактивен, возвращается 404 с detail.
