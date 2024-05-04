from apscheduler.schedulers.blocking import BlockingScheduler
from main import *

#trading_job()
scheduler = BlockingScheduler()
#scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='09')
scheduler.add_job(main, 'cron', day_of_week='mon-sun', hour='23', minute='16')
print("start")
scheduler.start()
print("stop")