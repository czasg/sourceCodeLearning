# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler

sch = BlockingScheduler()


def my_job1(): print("Hello world1")


def my_job2(): print("hello world2")


@sch.scheduled_job('interval', id='my_job3', seconds=2)  # 或者可以通过装饰器来实现
def my_job3(): print("hello world3")


# 直接指定执行周期，不会停止
sch.add_job(my_job1, 'interval', seconds=2, jitter=120)  # jitter是振动参数，每周期会随机增加浮动秒数

# start_date 指定开始时间与结束时间
sch.add_job(my_job2, 'interval', seconds=2, start_date='2019-12-30 09:50:00', end_date='2019-12-30 10:00:00')
sch.start()
