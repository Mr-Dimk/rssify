"""
Скрипт для тестирования создания и удаления записей в БД.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Site, Post

def test_create_and_delete():
    db = SessionLocal()
    try:
        # Создание тестового сайта
        site = Site(name="Test Site", url="https://example.com", selector=".post")
        db.add(site)
        db.commit()
        db.refresh(site)
        print(f"Создан сайт: {site.id}, {site.name}")

        # Создание тестового поста
        post = Post(site_id=site.id, title="Test Post", description="Desc", url="https://example.com/post")
        db.add(post)
        db.commit()
        db.refresh(post)
        print(f"Создан пост: {post.id}, {post.title}")

        # Проверка наличия записей
        site_check = db.query(Site).filter_by(id=site.id).first()
        post_check = db.query(Post).filter_by(id=post.id).first()
        assert site_check is not None, "Site not found after insert"
        assert post_check is not None, "Post not found after insert"

        # Удаление записей
        db.delete(post)
        db.delete(site)
        db.commit()
        print("Удалены тестовые записи.")

        # Проверка удаления
        assert db.query(Post).filter_by(id=post.id).first() is None, "Post not deleted"
        assert db.query(Site).filter_by(id=site.id).first() is None, "Site not deleted"
        print("Тест создания и удаления записей ПРОЙДЕН.")
    finally:
        db.close()

if __name__ == "__main__":
    test_create_and_delete()
