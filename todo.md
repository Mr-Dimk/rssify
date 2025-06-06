# RSSify - Пошаговый план разработки

> Детальный чеклист для создания сервиса RSSify от нуля до деплоя

## 🚀 Этап 1: Базовая настройка проекта

### 1.1 Инициализация проекта

- [x] 1.1.1. Создать репозиторий GitHub
- [x] 1.1.2. Клонировать репозиторий локально
- [x] 1.1.3. Создать структуру папок (app/, tests/, config/, logs/)
- [x] 1.1.4. Создать подпапки в app/ (routers/, templates/, static/)
- [x] 1.1.5. Инициализировать git и сделать первый коммит

### 1.2 Настройка окружения

- [x] 1.2.1. Создать файл requirements.txt с зависимостями
- [x] 1.2.2. Создать файл .env для конфигурации
- [x] 1.2.3. Создать файл .gitignore
- [x] 1.2.4. Создать виртуальное окружение Python
- [x] 1.2.5. Установить зависимости из requirements.txt

### 1.3 Базовые файлы

- [x] 1.3.1. Создать app/init.py
- [x] 1.3.2. Создать app/main.py (пустой FastAPI app)
- [x] 1.3.3. Проверить запуск uvicorn app.main:app --reload
- [x] 1.3.4. Убедиться что FastAPI docs доступны на /docs

---

## 🗄️ Этап 2: База данных и модели

### 2.1 Настройка базы данных

- [x] 2.1.1. Создать app/database.py
- [x] 2.1.2. Настроить подключение к SQLite
- [x] 2.1.3. Создать функцию get_db() для dependency injection
- [x] 2.1.4. Настроить Base для SQLAlchemy моделей

### 2.2 Модели данных

- [x] 2.2.1. Создать app/models.py
- [x] 2.2.2. Создать модель Site (id, name, url, selector, etc.)
- [x] 2.2.3. Создать модель Post (id, site_id, title, description, etc.)
- [x] 2.2.4. Настроить связи между моделями (Site -> Posts)
- [x] 2.2.5. Добавить индексы для оптимизации запросов

### 2.3 Pydantic схемы

- [x] 2.3.1. Создать app/schemas.py
- [x] 2.3.2. Создать SiteBase, SiteCreate, SiteUpdate схемы
- [x] 2.3.3. Создать PostBase, Post схемы
- [x] 2.3.4. Создать SiteWithPosts схему для вложенных данных
- [x] 2.3.5. Добавить валидацию полей (URL, длина строк)

### 2.4 Инициализация БД

- [x] 2.4.1. Создать скрипт создания таблиц
- [x] 2.4.2. Протестировать создание и удаление записей
- [x] 2.4.3. Добавить тестовые данные для разработки
- [x] Recreate the database tables from scratch and verify that the new selector fields are present in the `sites` table.
- [x] Run CRUD tests (`app/test_db_ops.py`) to confirm the schema is correct and the new fields are usable.

---

## 🕷️ Этап 3: Веб-скрапинг движок

### 3.1 Базовый скрапер

- [x] 3.1.1. Создать app/scraper.py
- [x] 3.1.2. Создать класс WebScraper
- [x] 3.1.3. Реализовать метод fetch_page() с requests + BeautifulSoup
- [x] 3.1.4. Добавить обработку ошибок HTTP запросов
- [x] 3.1.5. Настроить User-Agent и таймауты

### 3.2 Извлечение контента

- [x] 3.2.1. Реализовать метод extract_posts() с CSS селекторами
- [x] 3.2.2. Реализовать метод \_extract_single_post()
- [x] 3.2.3. Добавить извлечение заголовков, описаний, ссылок
- [x] 3.2.4. Реализовать создание хешей для дедупликации
- [x] 3.2.5. Добавить обработку относительных ссылок

### 3.3 Утилиты и валидация

- [x] 3.3.1. Создать app/utils.py
- [x] 3.3.2. Реализовать validate_url()
- [x] 3.3.3. Реализовать validate_css_selector()
- [x] 3.3.4. Добавить функции sanitize_filename(), truncate_text()
- [x] 3.3.5. Протестировать скрапинг на примере Claude Explains

---

## 📡 Этап 4: RSS генератор

### 4.1 Базовый RSS генератор

- [x] 4.1.1. Создать app/rss_generator.py
- [x] 4.1.2. Создать класс RSSGenerator с feedgen
- [x] 4.1.3. Реализовать метод generate_feed()
- [x] 4.1.4. Настроить метаданные фида (title, description, link)
- [x] 4.1.5. Добавить генерацию ID и временных меток

### 4.2 Форматирование постов

- [x] 4.2.1. Реализовать добавление постов в фид
- [x] 4.2.2. Настроить правильное форматирование title, description
- [x] 4.2.3. Обработать ссылки и pubDate
- [x] 4.2.4. Добавить ограничение количества постов в фиде
- [x] 4.2.5. Протестировать валидность генерируемого RSS

### 4.3 Дополнительные форматы

- [x] 4.3.1. Реализовать generate_atom_feed() для Atom формата
- [x] 4.3.2. Добавить поддержку кастомных полей
- [x] 4.3.3. Настроить корректную кодировку UTF-8
- [x] 4.3.4. Добавить обработку HTML тегов в описаниях

---

## 🌐 Этап 5: FastAPI API endpoints

### 5.1 Sites API

- [x] 5.1.1. Создать app/routers/sites.py
- [x] 5.1.2. Реализовать GET /api/sites (список сайтов)
- [x] 5.1.3. Реализовать GET /api/sites/{id} (конкретный сайт)
- [x] 5.1.4. Реализовать POST /api/sites (создание сайта)
- [x] 5.1.5. Реализовать PUT /api/sites/{id} (обновление сайта)
- [x] 5.1.6. Реализовать DELETE /api/sites/{id} (удаление сайта)

### 5.2 Feeds API

- [x] 5.2.1. Создать app/routers/feeds.py
- [x] 5.2.2. Реализовать GET /feed/{site_id} (RSS фид)
- [x] 5.2.3. Реализовать GET /feed/{site_id}/atom (Atom фид)
- [x] 5.2.4. Добавить правильные HTTP заголовки для XML
- [x] 5.2.5. Добавить обработку ошибок (сайт не найден, неактивен)

### 5.3 Административные endpoints

- [x] 5.3.1. Реализовать POST /api/sites/{id}/check (принудительная проверка)
- [x] 5.3.2. Реализовать GET /api/stats (статистика сервиса)
- [x] 5.3.3. Реализовать GET /health (healthcheck)
- [x] 5.3.4. Добавить endpoint для просмотра логов
- [x] 5.3.5. Подключить роуты к основному FastAPI приложению

---

## ⏰ Этап 6: Планировщик задач

### 6.1 Базовый планировщик

- [x] 6.1.1. Создать app/scheduler.py
- [x] 6.1.2. Настроить APScheduler с BackgroundScheduler
- [x] 6.1.3. Создать класс TaskScheduler
- [x] 6.1.4. Реализовать метод start_scheduler()
- [x] 6.1.5. Добавить graceful shutdown для планировщика

### 6.2 Задачи мониторинга

- [x] 6.2.1. Создать функцию check_site()
- [x] 6.2.2. Реализовать check_all_sites() с циклом по активным сайтам
- [x] 6.2.3. Добавить логику сохранения новых постов в БД
- [x] 6.2.4. Реализовать обновление last_check и last_error
- [x] 6.2.5. Добавить дедупликацию по content_hash

### 6.3 Настройка расписания

- [x] 6.3.1. Настроить периодический запуск check_all_sites()
- [x] 6.3.2. Добавить индивидуальные интервалы для каждого сайта
- [x] 6.3.3. Реализовать exponential backoff при ошибках
- [x] 6.3.4. Добавить максимальное время выполнения задач
- [x] 6.3.5. Интегрировать планировщик с FastAPI lifecycle

---

## 🐳 Этап 7: Docker и развертывание

### 7.1 Контейнеризация

- [x] 7.1.1. Создать Dockerfile для Python приложения
- [x] 7.1.2. Оптимизировать Dockerfile (multi-stage build)
- [x] 7.1.3. Создать docker-compose.yml
- [x] 7.1.4. Настроить volume для SQLite базы данных

### 7.3 Продакшн настройки

- [x] 7.3.1. Создать production.env с безопасными настройками
- [x] Удалить traefik из docker-compose.yml для локального запуска
- [x] Deploy the application using Docker Compose with the production.env file, ensuring the app starts правильно и checking the logs for successful startup.
- [ ] 7.3.2. Настроить логирование в файлы
- [ ] 7.3.3. Добавить health checks в docker-compose
- [ ] 7.3.4. Создать скрипт для бэкапа базы данных
- [ ] 7.3.5. Протестировать запуск через docker-compose up

---

## 🧪 Этап 8: Тестирование

> ⚠️ Блок 8.3 (CI/CD) временно отложен, перенесён в конец плана как будущее улучшение.

### 8.1 Unit тесты

- [x] 8.1.1. Настроить pytest в requirements.txt
- [x] 8.1.2. Создать tests/conftest.py с фикстурами
- [x] 8.1.3. Создать tests/test_scraper.py
- [x] 8.1.4. Создать tests/test_rss_generator.py
- [x] 8.1.5. Создать tests/test_utils.py
- [x] Добавить юнит-тесты для scheduler.py

### 8.2 Integration тесты

- [x] 8.2.1. Создать tests/test_api.py для API endpoints
- [x] 8.2.2. Протестировать CRUD операции с сайтами
- [x] 8.2.3. Протестировать генерацию RSS фидов
- [x] 8.2.4. Создать mock'и для внешних HTTP запросов
- [x] 8.2.5. Добавить тесты для планировщика

---

## 🚀 Этап 10+: Будущие улучшения

### 10.x CI/CD и автоматизация

- [ ] 8.3.1. Создать .github/workflows/test.yml
- [ ] 8.3.2. Настроить автоматические тесты на PR
- [ ] 8.3.3. Добавить coverage reporting
- [ ] 8.3.4. Настроить линтеры (black, flake8)
- [ ] 8.3.5. Добавить security сканирование dependencies

---

## 🎨 Этап 9: Веб-интерфейс (опционально)

### 9.1 Базовый UI

- [x] 9.1.1. Настроить Jinja2 templates в FastAPI
- [x] 9.1.2. Создать базовый HTML шаблон
- [x] 9.1.3. Создать страницу списка сайтов (теперь это index)
- [x] 9.1.4. Создать форму добавления нового сайта
- [x] 9.1.5. Добавить CSS стили (Bootstrap или TailwindCSS)

### 9.2 Интерактивность

- [x] 9.2.1. Добавить JavaScript для AJAX запросов
- [x] 9.2.2. Реализовать удаление сайтов без перезагрузки
- [x] 9.2.3. Добавить валидацию форм на клиенте
- [x] Реализовать логику кнопки редактирования сайта (модальное окно + AJAX)
- [x] 9.2.4. Показать статус последней проверки сайтов
- [x] 9.2.5. Добавить кнопку "Проверить сейчас"

---

## 🚀 Этап 10: Улучшения и оптимизация

### 10.1 Производительность

- [ ] 10.1.1. Добавить кеширование RSS фидов (Redis опционально)
- [ ] 10.1.2. Оптимизировать SQL запросы с eager loading
- [ ] 10.1.3. Добавить пагинацию для больших списков
- [ ] 10.1.4. Реализовать параллельную проверку сайтов
- [ ] 10.1.5. Добавить мониторинг производительности

### 10.2 Безопасность

- [ ] 10.2.1. Добавить API ключи для административных функций
- [ ] 10.2.2. Реализовать rate limiting для API
- [ ] 10.2.3. Добавить валидацию и санитизацию всех входных данных
- [ ] 10.2.4. Настроить CORS для веб-интерфейса
- [ ] 10.2.5. Добавить защиту от SSRF атак

### 10.3 Мониторинг

- [ ] 10.3.1. Интегрировать structured logging (JSON формат)
- [ ] 10.3.2. Добавить метрики для Prometheus (опционально)
- [ ] 10.3.3. Настроить алерты на критические ошибки
- [ ] 10.3.4. Создать dashboard для мониторинга
- [ ] 10.3.5. Добавить уведомления о недоступности сайтов

---

## 🌟 Этап 11: Расширенные возможности

### 11.1 Дополнительный функционал

- [ ] 11.1.1. Добавить поддержку webhook'ов для уведомлений
- [ ] 11.1.2. Реализовать фильтрацию постов по ключевым словам
- [ ] 11.1.3. Добавить категории для сайтов
- [ ] 11.1.4. Реализовать экспорт/импорт конфигураций
- [ ] 11.1.5. Добавить поддержку нескольких селекторов на одном сайте

### 11.2 Интеграции

- [ ] 11.2.1. Добавить отправку в Telegram через бота
- [ ] 11.2.2. Интеграция с Discord webhook'ами
- [ ] 11.2.3. Поддержка отправки email уведомлений
- [ ] 11.2.4. Интеграция с популярными RSS ридерами
- [ ] 11.2.5. API для интеграции с внешними сервисами

---

## 📚 Этап 12: Документация и релиз

### 12.1 Документация

- [ ] 12.1.1. Дополнить README.md с примерами использования
- [ ] 12.1.2. Создать API документацию (дополнить автогенерацию)
- [ ] 12.1.3. Написать guide по настройке селекторов
- [ ] 12.1.4. Создать CONTRIBUTING.md для контрибьюторов
- [ ] 12.1.5. Добавить примеры конфигураций для популярных сайтов

### 12.2 Релиз

- [ ] 12.2.1. Настроить semantic versioning
- [ ] 12.2.2. Создать CHANGELOG.md
- [ ] 12.2.3. Подготовить Docker образ для Docker Hub
- [ ] 12.2.4. Создать GitHub Release с бинарными файлами
- [ ] 12.2.5. Написать blog post или статью о проекте

---

## ✅ Чеклист готовности к продакшну

- [ ] Все unit и integration тесты проходят
- [ ] Docker контейнер собирается и запускается без ошибок
- [ ] RSS фиды валидируются в RSS валидаторах
- [ ] API документация актуальна и полная
- [ ] Настроено логирование и мониторинг
- [ ] Выполнены базовые security проверки
- [ ] Протестирована работа на нескольких различных сайтах
- [ ] Настроен CI/CD pipeline
- [ ] Создана документация для развертывания
- [ ] Проведен code review основных компонентов

**Примерное время разработки:** 2-3 недели для полной реализации одним разработчиком.
