from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

sch = BlockingScheduler()
now = datetime.now()
next = now + timedelta(seconds=10)


def my_job(text):
    print("hello world")


sch.add_job(my_job, 'date', run_date=next, args=['text'])  # run_date='2019-12-30 16:30:05' / 未指定时间, 则会立即执行
sch.start()
