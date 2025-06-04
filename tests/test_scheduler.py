import pytest
from app.scheduler import TaskScheduler
from unittest.mock import MagicMock

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
