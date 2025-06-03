import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Тестовый скрипт для проверки извлечения постов с помощью WebScraper.extract_posts
"""
from app.scraper import WebScraper

if __name__ == "__main__":
    url = "https://www.anthropic.com/engineering"
    post_selector = "article"  # пример: заменить на актуальный селектор для постов
    title_selector = "h2, h3"
    desc_selector = "p"
    link_selector = "a"

    scraper = WebScraper()
    try:
        soup = scraper.fetch_page(url)
        posts = scraper.extract_posts(
            soup,
            post_selector=post_selector,
            title_selector=title_selector,
            desc_selector=desc_selector,
            link_selector=link_selector,
            base_url=url
        )
        print(f"Извлечено постов: {len(posts)}")
        for i, post in enumerate(posts, 1):
            print(f"--- Post {i} ---")
            print(f"Title: {post['title']}")
            print(f"Description: {post['description']}")
            print(f"URL: {post['url']}")
            print(f"Hash: {post['content_hash']}")
    except Exception as e:
        print(f"Ошибка при скрапинге: {e}")
