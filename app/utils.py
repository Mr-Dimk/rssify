"""
Утилиты для валидации и вспомогательных операций в RSSify.
"""
import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Проверяет, является ли строка валидным URL.
    :param url: URL для проверки
    :return: True если валидный, иначе False
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False

def validate_css_selector(selector: str) -> bool:
    """
    Проверяет, является ли строка потенциально валидным CSS-селектором (простая проверка).
    :param selector: CSS-селектор
    :return: True если выглядит валидно, иначе False
    """
    # Примитивная проверка: не пустой, не слишком длинный, не содержит запрещённых символов
    if not selector or not isinstance(selector, str):
        return False
    if len(selector) > 256:
        return False
    # Не допускаем явно некорректные символы (например, пробелы в начале, управляющие символы)
    if selector.strip() != selector:
        return False
    if any(ord(c) < 32 for c in selector):
        return False
    # Минимальная проверка на допустимые символы CSS (буквы, цифры, . # > : [ ] и т.д.)
    if not re.match(r'^[\w\s\.#:>\[\]=\-_,\*\+~\(\)]+$', selector):
        return False
    return True

def sanitize_filename(filename: str, max_length: int = 128) -> str:
    """
    Очищает строку для безопасного использования в качестве имени файла.
    :param filename: исходное имя
    :param max_length: максимальная длина
    :return: безопасное имя файла
    """
    # Удаляем запрещённые символы для файловых имён
    filename = re.sub(r'[\\/:*?"<>|]', '', filename)
    filename = filename.strip().replace(' ', '_')
    return filename[:max_length]

def truncate_text(text: str, max_length: int = 256, suffix: str = '...') -> str:
    """
    Обрезает текст до max_length символов, добавляя суффикс если нужно.
    :param text: исходный текст
    :param max_length: максимальная длина
    :param suffix: суффикс для длинных текстов
    :return: обрезанный текст
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
