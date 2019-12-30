from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import CategoryForm, SiteEditForm, SiteForm
from core.models import Category, Site


def home(request):
    if request.user.is_authenticated:
        return redirect("core:site_read")
    return render(request, "core/home.html")


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.user, request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            Category(name=name, user=request.user).save()
            messages.success(request, "Entry sucessfully saved.")
            return redirect("core:category_management")
    else:
        form = CategoryForm(request.user)
    return render(request, "core/category_create.html", {"form": form})


@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = CategoryForm(request.user, request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Entry sucessufully modified.")
        return redirect("core:category_management")
    return render(request, "core/category_create.html", {"form": form})


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, "Entry sucessfully deleted.")
    return redirect("core:category_management")


@login_required
def category_management(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "core/category_management.html", {"categories": categories})


@login_required
def site_read(request):
    non_expired_sites = Site.objects.filter(Q(user=request.user) & Q(expired=False))
    expired_sites_count = Site.objects.filter(
        Q(user=request.user) & Q(expired=True)
    ).count()
    categories = Category.objects.all()
    total_categories = {}
    for category in categories:
        total = Site.objects.filter(
            Q(category__name=category) & Q(user=request.user) & Q(expired=False)
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


@login_required
def site_filter_category(request, category):
    try:
        sites = Site.objects.filter(
            Q(category__name=category) & Q(user=request.user) & Q(expired=False)
        )
    except Site.DoesNotExist:
        raise Http404("Not a valid category")
    total = Site.objects.filter(
        Q(category__name=category) & Q(user=request.user) & Q(expired=False)
    ).count()
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
        {
            "sites": sites,
            "total_categories": {},
            "total_expired": total,
            "total_overview": total,
        },
    )


@login_required
def sites_create(request):
    if request.method == "POST":
        form = SiteForm(request.user, request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            deadline = form.cleaned_data["deadline"]
            now = str(datetime.today().strftime("%a%b%d%H:%M:%S%Y"))
            image_name = "".join([request.user.username, "_", now, "_image.png"])
            Site(
                category=category,
                deadline=deadline,
                image_path=image_name,
                url=url,
                user=request.user,
            ).save()
            messages.success(request, "Entry sucessfully saved - Saving a screen shot")
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
    if request.method == "POST":
        form = SiteEditForm(request.user, request.POST or None, instance=site)
        if form.is_valid():
            site = form.save()
            messages.success(request, "Entry sucessfully modified")
            return redirect("core:site_management")
    else:
        form = SiteEditForm(request.user, instance=site)
        return render(request, "core/site_create.html", {"form": form})


@login_required
def site_delete(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    site.delete()
    messages.success(request, "Entry sucessfully deleted.")
    return redirect("core:site_read")
