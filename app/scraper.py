"""
Базовый модуль для веб-скрапинга.
"""

import requests
from bs4 import BeautifulSoup
import hashlib
from urllib.parse import urljoin

class WebScraper:
    """
    Класс для базового веб-скрапинга страниц.
    """
    def __init__(self, user_agent: str = None, timeout: int = 10):
        """
        :param user_agent: User-Agent для HTTP-запросов
        :param timeout: Таймаут для запросов (секунды)
        """
        self.user_agent = user_agent or "Mozilla/5.0 (compatible; RSSifyBot/1.0)"
        self.timeout = timeout

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Загружает страницу по URL и возвращает объект BeautifulSoup.
        :param url: URL страницы
        :return: BeautifulSoup или возбуждает исключение при ошибке
        """
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            # Логируем ошибку и пробрасываем дальше
            print(f"[WebScraper] Ошибка при запросе {url}: {e}")
            raise
        return BeautifulSoup(response.text, "html.parser")

    def extract_posts(self, soup: BeautifulSoup, post_selector: str, title_selector=None, desc_selector=None, link_selector=None, base_url=None) -> list:
        """
        Извлекает список постов с заголовками, описаниями и ссылками.
        :param soup: BeautifulSoup страницы
        :param post_selector: CSS-селектор для контейнера поста
        :param title_selector: CSS-селектор для заголовка (относительно post_tag)
        :param desc_selector: CSS-селектор для описания (относительно post_tag)
        :param link_selector: CSS-селектор для ссылки (относительно post_tag)
        :param base_url: Базовый URL для обработки относительных ссылок
        :return: Список словарей с ключами title, description, url
        """
        posts = []
        for tag in soup.select(post_selector):
            post_data = self._extract_single_post(
                tag,
                title_selector=title_selector,
                desc_selector=desc_selector,
                link_selector=link_selector,
                base_url=base_url
            )
            posts.append(post_data)
        return posts

    def _extract_single_post(self, post_tag, title_selector=None, desc_selector=None, link_selector=None, base_url=None):
        """
        Извлекает данные одного поста из тега по селекторам.
        :param post_tag: Tag (элемент поста)
        :param title_selector: CSS-селектор для заголовка (относительно post_tag)
        :param desc_selector: CSS-селектор для описания (относительно post_tag)
        :param link_selector: CSS-селектор для ссылки (относительно post_tag)
        :param base_url: Базовый URL для обработки относительных ссылок
        :return: dict с ключами title, description, url
        """
        title = None
        description = None
        url = None
        if title_selector:
            title_tag = post_tag.select_one(title_selector)
            title = title_tag.get_text(strip=True) if title_tag else None
        if desc_selector:
            desc_tag = post_tag.select_one(desc_selector)
            description = desc_tag.get_text(strip=True) if desc_tag else None
        if link_selector:
            link_tag = post_tag.select_one(link_selector)
            if link_tag and link_tag.has_attr('href'):
                url = link_tag['href']
                if base_url and url and not url.lower().startswith(('http://', 'https://')):
                    url = urljoin(base_url, url)
        # Генерация хеша для дедупликации (по title+description+url)
        hash_input = (title or "") + (description or "") + (url or "")
        content_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest() if hash_input else None
        return {"title": title, "description": description, "url": url, "content_hash": content_hash}
