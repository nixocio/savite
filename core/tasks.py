from celery import shared_task

from core.models import Site


@shared_task(name="deadline_expired")
def deadline_date():
    sites = Site.objects.all()
    for site in sites:
        print(site)
        if site.is_deadline_expired:
            site.expired = True
            site.save()
