from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

"""
class apscheduler.triggers.cron.CronTrigger(
year=None, 
month=None, 
day=None, 
week=None, 
day_of_week=None, 
hour=None, 
minute=None,
second=None, 
start_date=None, 
end_date=None, 
timezone=None, 
jitter=None)

"""

sch = BlockingScheduler()
bac = BackgroundScheduler()


def my_job(): print("hello world")


# sch.add_job(my_job, 'cron', month='1-6,6-12', day='1-30', hour='0-24')
# sch.start()

sch.add_job(my_job, 'cron', second="55")
sch.start()
