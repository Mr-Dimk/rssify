import pytest
from app.scheduler import TaskScheduler, check_site
from app.models import Site
from app.scraper import WebScraper
from app.database import SessionLocal

class DummyScraper(WebScraper):
    def fetch_page(self, url, timeout=10):
        # Возвращаем заранее подготовленный HTML
        return "<html><body><h2>Mock Post</h2><p>Mock Desc</p><a href='https://mock/post'></a></body></html>"

    def extract_posts(self, html, *args, **kwargs):
        # Возвращаем один мок-пост
        return [{
            'title': 'Mock Post',
            'description': 'Mock Desc',
            'url': 'https://mock/post',
            'pub_date': None
        }]

def test_scheduler_check_site_adds_post(monkeypatch):
    db = SessionLocal()
    try:
        # Создаём тестовый сайт
        site = Site(name="SchedulerTest", url="https://mock", selector="h2")
        db.add(site)
        db.commit()
        db.refresh(site)
        # Проверяем, что постов нет
        assert len(site.posts) == 0
        # Запускаем check_site с DummyScraper
        result = check_site(site, db, DummyScraper())
        db.refresh(site)
        db.expire_all()
        # Проверяем, что пост появился
        site = db.query(Site).filter_by(id=site.id).first()
        assert len(site.posts) == 1
        assert site.posts[0].title == 'Mock Post'
        # Чистим за собой
        db.delete(site.posts[0])
        db.delete(site)
        db.commit()
    finally:
        db.close()
