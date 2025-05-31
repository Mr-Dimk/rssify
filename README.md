# RSSify 📡

> Превращай любой сайт в RSS-фид! Универсальный сервис для мониторинга веб-страниц и автоматической генерации RSS-рассылок.

## 🚀 Что это такое?

RSSify отслеживает указанные веб-страницы на предмет новых публикаций и автоматически генерирует RSS-фиды. Идеально подходит для блогов и сайтов, у которых нет собственной RSS-подписки.

### ✨ Основные возможности

- 🔍 **Умный мониторинг** - автоматическое отслеживание изменений на веб-страницах
- 📰 **RSS генерация** - создание валидных RSS/Atom фидов
- ⚙️ **Гибкие настройки** - настраиваемые селекторы для разных типов сайтов
- 🕐 **Планировщик** - автоматические проверки по расписанию
- 🌐 **REST API** - полное управление через API
- 📊 **Веб-интерфейс** - простая админка для управления сайтами

## 🛠 Технологический стек

- **Python 3.11+** - основной язык
- **FastAPI** - веб-фреймворк с автодокументацией
- **SQLite** - легковесная база данных
- **Beautiful Soup 4** - парсинг HTML
- **Docker** - контейнеризация
- **Traefik** - рекомендуется для reverse proxy

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/rssify.git
cd rssify

# Запуск через Docker Compose
docker-compose up --build

# Сервис будет доступен по адресу http://localhost:8000
```

### Первое использование

1. Откройте API документацию: http://localhost:8000/docs
2. Добавьте сайт для мониторинга:
   ```bash
   curl -X POST "http://localhost:8000/api/sites" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://example.com/blog",
       "name": "Example Blog",
       "selector": "article h2"
     }'
   ```
3. Получите RSS-фид: http://localhost:8000/feed/{site_id}

## 📖 Использование

### Добавление сайта для мониторинга

```python
import requests

data = {
    "url": "https://www.anthropic.com/claude-explains",
    "name": "Claude Explains",
    "selector": "h3",  # CSS селектор для заголовков постов
    "description_selector": "p",  # Опционально: селектор описания
    "check_interval": 60  # Интервал проверки в минутах
}

response = requests.post("http://localhost:8000/api/sites", json=data)
site_id = response.json()["id"]
```

### Получение RSS-фида

RSS-фид доступен по адресу:

```
http://localhost:8000/feed/{site_id}
```

Можно добавить в любой RSS-ридер (Feedly, Inoreader, и т.д.)

### API Endpoints

| Endpoint          | Метод  | Описание                         |
| ----------------- | ------ | -------------------------------- |
| `/api/sites`      | GET    | Список всех отслеживаемых сайтов |
| `/api/sites`      | POST   | Добавить новый сайт              |
| `/api/sites/{id}` | GET    | Информация о сайте               |
| `/api/sites/{id}` | PUT    | Обновить настройки сайта         |
| `/api/sites/{id}` | DELETE | Удалить сайт                     |
| `/feed/{id}`      | GET    | RSS-фид для сайта                |
| `/health`         | GET    | Статус сервиса                   |

## 🔧 Конфигурация

### Переменные окружения

```env
# .env файл
DATABASE_URL=sqlite:///./rssify.db
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=1048576  # 1MB
DEFAULT_CHECK_INTERVAL=60   # минуты
MAX_FEED_ITEMS=50
```

### Пример настройки для популярных сайтов

```yaml
# config/presets.yml
anthropic_claude_explains:
  selector: 'h3'
  description_selector: 'p'
  link_selector: 'a'

medium_blog:
  selector: 'article h3'
  description_selector: 'article p'

dev_to:
  selector: '.crayons-story__title'
  description_selector: '.crayons-story__tags'
```

## 🏗 Разработка

### Локальная разработка

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск в режиме разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Структура проекта

```
rssify/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── models.py            # SQLAlchemy модели
│   ├── database.py          # Подключение к БД
│   ├── scraper.py           # Веб-скрапинг логика
│   ├── rss_generator.py     # Генерация RSS
│   ├── scheduler.py         # Планировщик задач
│   └── routers/
│       ├── __init__.py
│       ├── sites.py         # API для управления сайтами
│       └── feeds.py         # API для RSS фидов
├── tests/
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Тестирование

```bash
# Запуск тестов
pytest

# Тесты с покрытием
pytest --cov=app tests/
```

## 🚀 Развертывание

### Docker (рекомендуется)

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### VPS развертывание

1. Клонируйте репозиторий на сервер
2. Настройте Traefik как reverse proxy (рекомендуется)
3. Запустите через Docker Compose
4. Настройте SSL сертификат (Let's Encrypt)

## 🤝 Вклад в разработку

1. Сделайте fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

- 📖 [Документация API](http://localhost:8000/docs)
- 🐛 [Сообщить о баге](https://github.com/yourusername/rssify/issues)
- 💬 [Обсуждения](https://github.com/yourusername/rssify/discussions)

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) - потрясающий веб-фреймворк
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML парсинг
- [feedgen](https://github.com/lkiesow/python-feedgen) - генерация RSS фидов

---

**RSSify** - превращаем веб в RSS! 🚀📡
