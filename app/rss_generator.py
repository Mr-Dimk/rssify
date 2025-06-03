"""
Модуль для генерации RSS-фидов.
"""
# feedgen используется для генерации RSS/Atom
from feedgen.feed import FeedGenerator


class RSSGenerator:
    """
    Класс для генерации RSS-фидов с помощью feedgen.
    """

    def __init__(self, title: str, link: str, description: str, max_items: int = None):
        self.fg = FeedGenerator()
        self.fg.title(title)
        self.fg.link(href=link, rel="alternate")
        self.fg.description(description)
        self.fg.id(link)  # Atom требует id
        self._items = []
        self._max_items = max_items

    def generate_feed(self) -> str:
        """
        Генерирует RSS-фид в формате XML.
        :return: Строка с RSS XML
        """
        # Добавляем только последние max_items, если лимит задан
        if self._max_items is not None:
            items = self._items[-self._max_items:]
        else:
            items = self._items
        # Очищаем feed перед повторной генерацией
        self.fg._FeedGenerator__entries = []
        for item in items:
            self._add_entry_to_feed(**item)
        return self.fg.rss_str(pretty=True).decode("utf-8")

    def generate_atom_feed(self) -> str:
        """
        Генерирует Atom-фид в формате XML.
        :return: Строка с Atom XML
        """
        if self._max_items is not None:
            items = self._items[-self._max_items:]
        else:
            items = self._items
        self.fg._FeedGenerator__entries = []
        for item in items:
            self._add_entry_to_feed(**item)
        return self.fg.atom_str(pretty=True).decode("utf-8")

    def set_metadata(self, title: str = None, link: str = None, description: str = None, language: str = None):
        """
        Позволяет обновить метаданные фида (title, description, link, language).
        """
        if title:
            self.fg.title(title)
        if link:
            self.fg.link(href=link, rel="alternate")
        if description:
            self.fg.description(description)
        if language:
            self.fg.language(language)

    def add_item(self, title: str, link: str, description: str = None, guid: str = None, pubdate = None, author: str = None, category: str = None, html_description: bool = False, **custom_fields):
        """
        Добавляет элемент (пост) в RSS/Atom-фид с поддержкой кастомных полей.
        :param title: Заголовок поста
        :param link: Ссылка на пост
        :param description: Описание поста
        :param guid: Уникальный идентификатор (если не задан — используется link)
        :param pubdate: Дата публикации (datetime или str)
        :param author: Автор поста (опционально)
        :param category: Категория поста (опционально)
        :param html_description: Описание содержит HTML (CDATA)
        :param custom_fields: Любые дополнительные поля
        """
        self._items.append({
            "title": title,
            "link": link,
            "description": description,
            "guid": guid,
            "pubdate": pubdate,
            "author": author,
            "category": category,
            "html_description": html_description,
            "custom_fields": custom_fields
        })

    def _add_entry_to_feed(self, title, link, description=None, guid=None, pubdate=None, author=None, category=None, html_description=False, custom_fields=None):
        entry = self.fg.add_entry()
        entry.title(str(title))
        entry.link(href=str(link))
        if description:
            if html_description:
                entry.content(description, type="html")
            else:
                entry.description(str(description))
        entry.guid(guid or link, permalink=True)
        if pubdate:
            # Приводим pubdate к datetime с tzinfo (UTC), если это строка без tzinfo
            from datetime import datetime, timezone
            if isinstance(pubdate, str):
                try:
                    dt = datetime.fromisoformat(pubdate)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    entry.pubDate(dt)
                except Exception:
                    entry.pubDate(pubdate)  # пусть feedgen сам обработает
            elif isinstance(pubdate, datetime):
                if pubdate.tzinfo is None:
                    pubdate = pubdate.replace(tzinfo=timezone.utc)
                entry.pubDate(pubdate)
            else:
                entry.pubDate(pubdate)
        if author:
            entry.author({'name': author})
        if category:
            entry.category(term=category)
        if custom_fields:
            for k, v in custom_fields.items():
                entry.category(term=f"{k}:{v}")
