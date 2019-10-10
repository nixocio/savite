import os
import urllib.parse as urlparse
from datetime import datetime
from pprint import pprint

from celery import shared_task
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options

from core.forms import SiteForm
from core.models import Category, Site


def site_read(request):
    sites = Site.objects.filter().all()
    non_expired_sites = Site.objects.filter(expired=False)
    expired_sites = Site.objects.filter(expired=True).count()
    categories = Category.objects.all()
    total_categories = {}
    for category in categories:
        total = Site.objects.filter(category__name=category).count()
        if total > 0:
            total_categories.update({category.name: total})
    return render(
        request,
        "core/sites_read.html",
        {
            "sites": sites,
            "total_categories": total_categories,
            "total_overview": sum(total_categories.values()),
            "total_expired": expired_sites,
        },
    )
    # TODO Add page explaining what to do
    # Perhaps add trending on a few sites...


@login_required
def site_filter_category(request, category):
    category = get_object_or_404(Category, name=category)
    try:
        sites = Site.objects.filter(category__name=category)
    except Site.DoesNotExist:
        raise Http404("test")
    total = Site.objects.filter(category__name=category).count()
    total_categories = {category: total}
    return render(
        request,
        "core/sites_read.html",
        {
            "sites": sites,
            "total_categories": total_categories,
            "total_overview": sum(total_categories.values()),
        },
    )


@login_required
def sites_create(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            deadline = form.cleaned_data["deadline"]
            now = str(datetime.today().timestamp())
            image_name = "".join([now, "_image.png"])
            get_screen_shot.delay(url, image_name)

            Site(
                category=category, deadline=deadline, image_path=image_name, url=url, user=request.user
            ).save()

            return redirect("core:site_management")
    else:
        form = SiteForm()
    return render(request, "core/site_create.html", {"form": form})


@login_required
def site_management(request):
    sites = Site.objects.filter(user=request.user)
    return render(request, "core/sites_management.html", {"sites": sites})


@login_required
def site_edit(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = SiteForm(request.POST or None, instance=site)
    if form.is_valid():
        form.save()
        return redirect("core:site_management")
    return render(request, "core/site_create.html", {"form": form})


@login_required
def site_delete(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    site.delete()
    return redirect("core:site_management")


@shared_task
def get_screen_shot(url, image_name, username=None):
    width = 400
    height = 600
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    driver.get(url)
    driver.set_window_size(width, height)
    img_dir = settings.MEDIA_ROOT
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    driver.save_screenshot(os.path.join(img_dir, image_name))
    driver.quit()
    return None
