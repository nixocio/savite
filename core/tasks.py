from celery import task

from core.models import Site

@task(name="deadline_expired")
def deadline_date():
    sites = Site.objects.all()
    for site in sites:
        if site.is_deadline_expired:
            site.expired = True
            site.save()
