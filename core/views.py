import os
import urllib.parse as urlparse
from datetime import datetime
from pprint import pprint

from celery import shared_task
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options

from core.forms import SiteForm
from core.models import Category, Site


def home(request):
    return render(request, "core/home.html")


@login_required
def site_read(request):
    sites = Site.objects.filter(user=request.user)
    non_expired_sites = Site.objects.filter(
        Q(user=request.user) & Q(expired=False))
    expired_sites_count = Site.objects.filter(
        Q(user=request.user) & Q(expired=True)).count()
    expired_sites = Site.objects.filter(Q(user=request.user) & Q(expired=True))
    categories = Category.objects.all()
    total_categories = {}
    for category in categories:
        total = Site.objects.filter(
            Q(category__name=category) & Q(
                user=request.user) & Q(expired=False)
        ).count()
        if total > 0:
            total_categories.update({category.name: total})
    return render(
        request,
        "core/sites_read.html",
        {
            "sites": non_expired_sites,
            "total_categories": total_categories,
            "total_overview": sum(total_categories.values()) + expired_sites_count,
            "total_expired": expired_sites_count,
        },
    )
    # TODO Add page explaining what to do
    # Perhaps add trending on a few sites...


@login_required
def site_filter_category(request, category):
    category = get_object_or_404(Category, name=category)
    try:
        sites = Site.objects.filter(Q(category__name=category) & Q(
            user=request.user) & Q(expired=False))
    except Site.DoesNotExist:
        raise Http404("Not a valid category")
    total = Site.objects.filter(Q(category__name=category) & Q(
        user=request.user) & Q(expired=False)).count()
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
def site_filter_expired(request):
    sites = Site.objects.filter(Q(user=request.user) & Q(expired=True))
    total = Site.objects.filter(Q(expired=True) & Q(user=request.user)).count()
    return render(
        request,
        "core/sites_read.html",
        {"sites": sites, "total_categories": {},
            "total_expired": total, "total_overview": total},
    )


@login_required
def sites_create(request):
    if request.method == "POST":
        form = SiteForm(request.user, request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            deadline = form.cleaned_data["deadline"]
            now = str(datetime.today().timestamp())
            image_name = "".join(
                [request.user.username, "_", now, "_image.png"])
            print(image_name)
            image_dir = create_user_dir(request.user.username)
            get_screen_shot.delay(url, image_dir, image_name)
            Site(
                category=category, deadline=deadline, image_path=image_name, url=url, user=request.user
            ).save()
            return redirect("core:site_management")
    else:
        form = SiteForm(request.user)
    return render(request, "core/site_create.html", {"form": form})


@login_required
def site_management(request):
    sites = Site.objects.filter(user=request.user)
    return render(request, "core/sites_management.html", {"sites": sites})


@login_required
def site_edit(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    user = request.user
    form = SiteForm(request.user, request.POST or None, instance=site)
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
def get_screen_shot(url, image_dir, image_name):
    width = 400
    height = 600
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    driver.get(url)
    driver.set_window_size(width, height)
    driver.save_screenshot(os.path.join(image_dir, image_name))
    driver.quit()
    return None


def create_user_dir(username):
    image_dir = os.path.join(settings.MEDIA_ROOT, username)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir
