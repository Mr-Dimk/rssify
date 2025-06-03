import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Скрипт для наполнения базы тестовыми данными для разработки.
"""
from app.database import SessionLocal
from app.models import Site, Post

def seed_data():
    db = SessionLocal()
    try:
        # Примеры сайтов
        sites = [
            Site(name="Habr", url="https://habr.com/ru/news/", selector=".tm-article-snippet"),
            Site(name="Python.org", url="https://www.python.org/blogs/", selector=".blog-widget .list-recent-posts li"),
        ]
        db.add_all(sites)
        db.commit()
        for site in sites:
            db.refresh(site)

        # Примеры постов
        posts = [
            Post(site_id=sites[0].id, title="Habr Post 1", description="Desc 1", url="https://habr.com/ru/post/1"),
            Post(site_id=sites[0].id, title="Habr Post 2", description="Desc 2", url="https://habr.com/ru/post/2"),
            Post(site_id=sites[1].id, title="Python Post 1", description="Desc 3", url="https://www.python.org/blogs/post1"),
        ]
        db.add_all(posts)
        db.commit()
        print("Тестовые данные успешно добавлены.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
