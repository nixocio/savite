import os
import urllib.parse as urlparse
from datetime import datetime
from pprint import pprint

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions

from core.forms import SiteForm
from core.models import Site
from users.forms import CustomUserChangeForm, CustomUserCreationForm


def site_read(request):
    sites = Site.objects.all()
    return render(request, "core/sites_read.html", {"sites": sites})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:sites_read")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def sites_create(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            deadline = form.cleaned_data["deadline"]
            pprint(url)
            image_path, image_name = get_screen_shot(url)

            Site(
                category=category,
                deadline=deadline,
                image_path=image_name,
                url=url,
                user=request.user,
            ).save()

            return redirect("core:site_management")
    else:
        form = SiteForm()
    return render(request, "core/site_create.html", {"form": form})


def get_screen_shot(url):
    width = 400
    height = 400
    options = ChromeOptions()
    options.headless = True
    # driver = Firefox(options=options)
    driver = Chrome(options=options)
    driver.get(url)
    driver.set_window_size(width, height)
    now = str(datetime.today().timestamp())
    img_dir = settings.MEDIA_ROOT
    img_name = "".join([now, "_image.png"])
    full_img_path = os.path.join(img_dir, img_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    driver.save_screenshot(full_img_path)
    driver.quit()
    return full_img_path, img_name


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
