from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pprint import pprint

from core.models import Site
from core.forms import SiteForm
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
            Site(url=url, category=category, user=request.user).save()
            return redirect("core:site_management")
    else:
        form = SiteForm()
    return render(request, "core/site_create.html", {"form": form})


def get_screen_shot(url):
    pass


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
