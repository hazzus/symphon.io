from apscheduler.schedulers.background import BackgroundScheduler
from concert_parser import views

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", minutes=60, replace_existing=True)
def test_job():
    print('updating')
    views.parse(None)


register_events(scheduler)

scheduler.start()
