import datetime
from apscheduler.schedulers.background import BlockingScheduler

SCHEDULER = BlockingScheduler()

def add_cron_job(job, hour: int, minute: int, args = None):
    SCHEDULER.add_job(job, 'cron', hour=hour, minute=minute, args=args)

def add_planned_job(job, run_date: datetime.datetime):
    SCHEDULER.add_job(job, 'date', run_date=run_date)

def start_scheduler():
    try:
        SCHEDULER.start()
    except (KeyboardInterrupt, SystemExit):
        pass