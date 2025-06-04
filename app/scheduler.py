"""
Task scheduler module for RSSify project.
Uses APScheduler for background job scheduling.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
import signal
import threading
import time

class TaskScheduler:
    """
    TaskScheduler manages background jobs using APScheduler.
    """
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        """Start the background scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self, wait=True):
        """Shutdown the scheduler gracefully."""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=wait)

    def add_job(self, func, trigger, **kwargs):
        """
        Add a job to the scheduler.
        :param func: Callable to schedule
        :param trigger: Trigger type (e.g., 'interval', 'cron')
        :param kwargs: Trigger and job options
        :return: Job instance
        """
        return self.scheduler.add_job(func, trigger, **kwargs)

    def start_scheduler(self):
        """
        Alias for start(), for compatibility with project task naming.
        """
        self.start()

    def graceful_shutdown(self, wait=True):
        """
        Gracefully shutdown the scheduler (alias for shutdown).
        Can be used in FastAPI shutdown event for clean exit.
        """
        self.shutdown(wait=wait)

def check_site(site, db_session, scraper, logger=None):
    """
    Проверяет сайт: скачивает страницу, извлекает посты, возвращает результат.
    :param site: объект Site (SQLAlchemy)
    :param db_session: сессия БД для записи результатов
    :param scraper: экземпляр WebScraper
    :param logger: опциональный логгер
    :return: dict с результатом проверки
    """
    print(f"[check_site] START: site.id={site.id}, url={site.url}")
    print(f"[check_site] SELECTORS: post={site.selector}, title={site.title_selector}, desc={site.desc_selector}, link={site.link_selector}")
    result = {"site_id": site.id, "success": False, "error": None, "posts": []}
    try:
        html = scraper.fetch_page(site.url)
        print(f"[check_site] fetch_page OK, type(html)={type(html)}")
        posts = scraper.extract_posts(
            html,
            post_selector=site.selector,
            title_selector=site.title_selector,
            desc_selector=site.desc_selector,
            link_selector=site.link_selector,
            base_url=site.url
        )
        print(f"[check_site] extract_posts OK, posts found: {len(posts)}")
        # --- Сохранение новых постов в БД ---
        from app.models import Post
        from sqlalchemy.exc import IntegrityError
        new_posts = []
        for post in posts:
            exists = db_session.query(Post).filter_by(site_id=site.id, content_hash=post.get('content_hash')).first()
            if not exists:
                new_post = Post(
                    site_id=site.id,
                    title=post.get('title'),
                    description=post.get('description'),
                    url=post.get('url'),
                    content_hash=post.get('content_hash'),
                    published_at=post.get('pub_date')  # <-- исправлено с pub_date на published_at
                )
                db_session.add(new_post)
                new_posts.append(new_post)
        try:
            db_session.commit()
            print(f"[check_site] DB commit OK, new_posts: {len(new_posts)}")
        except IntegrityError as e:
            db_session.rollback()
            print(f"[check_site] DB IntegrityError: {e}")
            if logger:
                logger.error(f"DB integrity error for site {site.id}: {e}")
        result["new_posts_count"] = len(new_posts)
        # --- Обновление last_check и last_error ---
        site.last_check = datetime.now(timezone.utc)
        site.last_error = None
        db_session.commit()
        result["posts"] = posts
        result["success"] = True
        print(f"[check_site] SUCCESS: site.id={site.id}, posts saved: {len(new_posts)}")
        if logger:
            logger.info(f"Site {site.id} checked successfully: {len(posts)} posts found.")
    except Exception as e:
        result["error"] = str(e)
        # --- Обновление last_error при ошибке ---
        site.last_error = str(e)
        site.last_check = datetime.now(timezone.utc)
        db_session.commit()
        print(f"[check_site] ERROR: {e}")
        if logger:
            logger.error(f"Error checking site {site.id}: {e}")
    return result

def check_all_sites(db_session, scraper, logger=None):
    """
    Проверяет все активные сайты из базы данных.
    :param db_session: сессия БД
    :param scraper: экземпляр WebScraper
    :param logger: опциональный логгер
    :return: список результатов по сайтам
    """
    from app.models import Site
    results = []
    sites = db_session.query(Site).filter_by(is_active=True).all()
    for site in sites:
        result = check_site(site, db_session, scraper, logger)
        results.append(result)
    return results

# --- Периодический запуск check_all_sites ---
def schedule_periodic_check_all_sites(scheduler: TaskScheduler, db_session_factory, scraper, logger=None, interval_minutes=10):
    """
    Добавляет периодическую задачу проверки всех сайтов в планировщик.
    :param scheduler: экземпляр TaskScheduler
    :param db_session_factory: функция для создания новой сессии БД
    :param scraper: экземпляр WebScraper
    :param logger: опциональный логгер
    :param interval_minutes: интервал в минутах
    """
    def job():
        db = db_session_factory()
        try:
            check_all_sites(db, scraper, logger)
        finally:
            db.close()
    scheduler.add_job(job, 'interval', minutes=interval_minutes, id='check_all_sites')

def schedule_individual_site_checks(scheduler: TaskScheduler, db_session_factory, scraper, logger=None):
    """
    Добавляет индивидуальные задачи проверки для каждого активного сайта с учетом их интервала.
    :param scheduler: экземпляр TaskScheduler
    :param db_session_factory: функция для создания новой сессии БД
    :param scraper: экземпляр WebScraper
    :param logger: опциональный логгер
    """
    db = db_session_factory()
    try:
        from app.models import Site
        sites = db.query(Site).filter_by(is_active=True).all()
        for site in sites:
            interval = getattr(site, 'check_interval', 10)  # default 10 min
            def make_job(site_id):
                def job():
                    db_local = db_session_factory()
                    try:
                        site_obj = db_local.query(Site).get(site_id)
                        check_site(site_obj, db_local, scraper, logger)
                    finally:
                        db_local.close()
                return job
            scheduler.add_job(
                make_job(site.id),
                'interval',
                minutes=interval,
                id=f'check_site_{site.id}',
                replace_existing=True
            )
    finally:
        db.close()

def get_backoff_delay(error_count, base=10, max_delay=180):
    """
    Вычисляет задержку для exponential backoff (в минутах).
    :param error_count: количество подряд ошибок
    :param base: базовый интервал (минуты)
    :param max_delay: максимальная задержка (минуты)
    :return: задержка в минутах
    """
    delay = base * (2 ** (error_count - 1))
    return min(delay, max_delay)

# --- Индивидуальный запуск с backoff ---
def schedule_individual_site_checks_with_backoff(scheduler: TaskScheduler, db_session_factory, scraper, logger=None):
    """
    Добавляет задачи проверки для каждого сайта с поддержкой exponential backoff при ошибках.
    """
    db = db_session_factory()
    try:
        from app.models import Site
        sites = db.query(Site).filter_by(is_active=True).all()
        for site in sites:
            def make_job(site_id):
                def job():
                    db_local = db_session_factory()
                    try:
                        site_obj = db_local.query(Site).get(site_id)
                        # Подсчет ошибок (например, site.error_count)
                        error_count = getattr(site_obj, 'error_count', 0)
                        result = check_site(site_obj, db_local, scraper, logger)
                        if result.get('success'):
                            site_obj.error_count = 0
                        else:
                            site_obj.error_count = error_count + 1
                        db_local.commit()
                        delay = get_backoff_delay(site_obj.error_count)
                        # Переназначить задачу с новым интервалом
                        scheduler.add_job(
                            make_job(site_id),
                            'interval',
                            minutes=delay,
                            id=f'check_site_{site_id}',
                            replace_existing=True
                        )
                    finally:
                        db_local.close()
                return job
            # Начальный запуск с обычным интервалом
            interval = getattr(site, 'check_interval', 10)
            scheduler.add_job(
                make_job(site.id),
                'interval',
                minutes=interval,
                id=f'check_site_{site.id}',
                replace_existing=True
            )
    finally:
        db.close()

def run_with_timeout(func, timeout_sec, *args, **kwargs):
    """
    Запускает функцию с таймаутом. Если функция не завершилась за timeout_sec, выбрасывает TimeoutError.
    Работает в отдельном потоке, безопасно для I/O-bound задач.
    """
    result = {}
    def target():
        try:
            result['value'] = func(*args, **kwargs)
        except Exception as e:
            result['error'] = e
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_sec)
    if thread.is_alive():
        raise TimeoutError(f"Task exceeded {timeout_sec} seconds")
    if 'error' in result:
        raise result['error']
    return result.get('value')

# --- Пример использования в планировщике ---
def schedule_site_check_with_timeout(scheduler: TaskScheduler, db_session_factory, scraper, logger=None, timeout_sec=60):
    """
    Добавляет задачу проверки всех сайтов с ограничением по времени выполнения.
    """
    def job():
        db = db_session_factory()
        try:
            run_with_timeout(lambda: check_all_sites(db, scraper, logger), timeout_sec)
        except TimeoutError as e:
            if logger:
                logger.error(f"Site check timeout: {e}")
        finally:
            db.close()
    scheduler.add_job(job, 'interval', minutes=10, id='check_all_sites_with_timeout', replace_existing=True)

# --- Интеграция планировщика с FastAPI lifecycle ---
def setup_scheduler_with_fastapi(app, db_session_factory, scraper, logger=None):
    """
    Интегрирует TaskScheduler с событиями запуска и завершения FastAPI.
    """
    scheduler = TaskScheduler()

    @app.on_event("startup")
    def on_startup():
        scheduler.start()
        # Можно выбрать нужную функцию планирования:
        # schedule_periodic_check_all_sites(scheduler, db_session_factory, scraper, logger)
        # schedule_individual_site_checks(scheduler, db_session_factory, scraper, logger)
        # schedule_individual_site_checks_with_backoff(scheduler, db_session_factory, scraper, logger)
        # schedule_site_check_with_timeout(scheduler, db_session_factory, scraper, logger, timeout_sec=60)
        schedule_periodic_check_all_sites(scheduler, db_session_factory, scraper, logger)

    @app.on_event("shutdown")
    def on_shutdown():
        scheduler.graceful_shutdown()

    return scheduler

# Example usage (to be integrated with FastAPI lifecycle):
# scheduler = TaskScheduler()
# scheduler.start()
