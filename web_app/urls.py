from django.contrib import admin
from django.urls import path, include

from core import views as core_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("signup/", core_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
