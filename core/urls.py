from django.contrib import admin
from django.urls import include, path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/delete/<int:category_id>", views.category_delete, name="category_delete"),
    path("category/edit/<int:category_id>", views.category_edit, name="category_edit"),
    path("category/general/management/", views.category_management, name="category_management"),
    path("site/create/", views.sites_create, name="site_create"),
    path("site/delete/<int:site_id>/", views.site_delete, name="site_delete"),
    path("site/edit/<int:site_id>/", views.site_edit, name="site_edit"),
    path(
        "site/filter/category/<str:category>/",
        views.site_filter_category,
        name="site_filter_category",
    ),
    path("site/filter/expired/", views.site_filter_expired, name="site_filter_expired"),
    path("site/general/management/", views.site_management, name="site_management"),
    path("site/read", views.site_read, name="site_read"),
]
