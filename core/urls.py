from django.contrib import admin
from django.urls import include, path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.sites_read, name="home"),
    path("site/create/", views.sites_create, name="site_create"),
    path("site/delete/<int:site_id>/", views.site_delete, name="site_delete"),
    # path("product/details/<int:product_id>/", views.product_details, name="product_details"),
    path("site/edit/<int:site_id>/", views.site_edit, name="site_edit"),
    path("site/management/", views.site_management, name="site_management"),
    path("signup/", views.signup, name="signup"),
]
