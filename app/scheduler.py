"""
Task scheduler module for RSSify project.
Uses APScheduler for background job scheduling.
"""

from apscheduler.schedulers.background import BackgroundScheduler

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

# Example usage (to be integrated with FastAPI lifecycle):
# scheduler = TaskScheduler()
# scheduler.start()
