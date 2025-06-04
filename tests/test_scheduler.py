import pytest
from app.scheduler import TaskScheduler, check_site, check_all_sites
from unittest.mock import MagicMock, patch

class DummySite:
    def __init__(self, id, url, selector):
        self.id = id
        self.url = url
        self.selector = selector
        self.last_check = None
        self.last_error = None

class DummyPost:
    def __init__(self, link, content_hash):
        self.link = link
        self.content_hash = content_hash

@pytest.fixture
def dummy_db_session():
    class DummyQuery:
        def __init__(self, posts):
            self._posts = posts
        def filter_by(self, **kwargs):
            # Simulate no duplicates
            return self
        def first(self):
            return None
        def all(self):
            return [DummySite(1, 'http://test', 'div.post')]
    class DummySession:
        def __init__(self):
            self.queries = []
            self.committed = False
        def query(self, model):
            return DummyQuery([])
        def add(self, obj):
            self.queries.append(obj)
        def commit(self):
            self.committed = True
        def rollback(self):
            pass
    return DummySession()

@pytest.fixture
def scheduler():
    sched = TaskScheduler()
    yield sched
    sched.shutdown(wait=False)

def test_start_and_shutdown(scheduler):
    scheduler.start()
    assert scheduler.scheduler.running
    scheduler.shutdown()
    assert not scheduler.scheduler.running

def test_add_job_runs_function(scheduler):
    mock_func = MagicMock()
    scheduler.start()
    job = scheduler.add_job(mock_func, 'interval', seconds=1, id='test_job')
    # Let the scheduler tick
    import time
    time.sleep(1.2)
    scheduler.shutdown()
    assert mock_func.called
    assert job.id == 'test_job'

def test_graceful_shutdown_alias(scheduler):
    scheduler.start()
    scheduler.graceful_shutdown()
    assert not scheduler.scheduler.running

def test_start_scheduler_alias(scheduler):
    scheduler.start_scheduler()
    assert scheduler.scheduler.running
    scheduler.shutdown()

def test_check_site_saves_new_posts(dummy_db_session):
    # Patch app.models.Post and datetime.now(datetime.UTC) to avoid DeprecationWarning
    import sys
    import types
    dummy_models = types.ModuleType('app.models')
    class DummyPost:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    dummy_models.Post = DummyPost
    sys.modules['app.models'] = dummy_models
    import datetime
    sys.modules['sqlalchemy.exc'] = types.SimpleNamespace(IntegrityError=Exception)
    # Patch datetime.now(datetime.UTC)
    orig_datetime = datetime.datetime
    class DummyDatetime(orig_datetime):
        @classmethod
        def now(cls, tz=None):
            return orig_datetime(2025, 1, 1, tzinfo=tz)
    datetime.datetime = DummyDatetime

    site = DummySite(1, 'http://test', 'div.post')
    scraper = MagicMock()
    scraper.fetch_page.return_value = '<html></html>'
    scraper.extract_posts.return_value = [
        {'title': 't', 'description': 'd', 'link': 'l', 'content_hash': 'h', 'pub_date': None}
    ]
    logger = MagicMock()
    result = check_site(site, dummy_db_session, scraper, logger)
    assert result['success']
    assert result['new_posts_count'] == 1
    assert dummy_db_session.committed
    logger.info.assert_called()
    # Cleanup
    datetime.datetime = orig_datetime
    del sys.modules['app.models']
    del sys.modules['sqlalchemy.exc']

def test_check_all_sites_calls_check_site(dummy_db_session):
    scraper = MagicMock()
    scraper.fetch_page.return_value = '<html></html>'
    scraper.extract_posts.return_value = []
    logger = MagicMock()
    with patch('app.scheduler.check_site', wraps=check_site) as check_site_mock:
        results = check_all_sites(dummy_db_session, scraper, logger)
        assert isinstance(results, list)
        check_site_mock.assert_called()
