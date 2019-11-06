from celery import shared_task, task
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

from core.models import Site


@task(name="deadline_expired")
def deadline_date():
    sites = Site.objects.all()
    for site in sites:
        if site.is_deadline_expired:
            site.expired = True
            site.save()
