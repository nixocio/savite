from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from api import api_views

app_name = "api"

urlpatterns = [
    path("list/categories", api_views.categories_list, name="categories_list"),
    path("create/site", api_views.create_site, name="create_site"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
