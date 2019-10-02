import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Career
# Podcast
# Productivity
# Linux
# Business
# Python
# Front-End
# Back-End
# Education


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Site(models.Model):
    url = models.URLField(verbose_name="Site URL", unique=True, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="categories"
    )
    image_path = models.CharField(max_length=300)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=False)

    @property
    def image_path_modified(self):
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image_path)):
            return self.image_path
        return "default_image.jpg"

    class Meta:
        ordering = ("-modified_at",)

    def __str__(self):
        return "{}"


@receiver(post_delete, sender=Site)
def remove_file(sender, instance, *args, **kwargs):
    file_path = os.path.join(settings.MEDIA_ROOT, instance.image_path)
    if os.path.exists(file_path):
        os.remove(file_path)
