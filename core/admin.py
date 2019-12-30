from django.contrib import admin

from core.models import Category, Site


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "modified_at",)
    list_filter = ("user", "name",)


class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "url",
        "user",
        "created_at",
        "modified_at",
        "deadline",
        "expired",
    )
    list_filter = ("category", "user", "url", "deadline", "expired")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Site, SiteAdmin)
