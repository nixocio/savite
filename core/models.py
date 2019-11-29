import os

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "categories"
        unique_together = ["name", "user"]

    def __str__(self):
        return self.name


def default_date():
    return timezone.now() + timezone.timedelta(days=30)


class Site(models.Model):
    url = models.URLField(verbose_name="Site URL", blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    image_path = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=default_date, blank=True)
    expired = models.BooleanField(default=False)

    @property
    def is_deadline_expired(self):
        return self.deadline < timezone.localtime(timezone.now())

    @property
    def image_path_modified(self):
        if os.path.isfile(
            os.path.join(
                os.path.join(settings.MEDIA_ROOT, "users"),
                os.path.join(self.user.username, self.image_path),
            )
        ):
            return os.path.join("users", self.user.username, self.image_path)
        return os.path.join("default", "default_image.jpg")

    class Meta:
        ordering = ("-modified_at",)
        unique_together = ("user", "url")

    def save(self, *args, **kwargs):
        if self.deadline < timezone.localtime(timezone.now()):
            raise ValidationError("Not a valid deadline.")

        image_dir = create_user_dir(self.user.username)
        get_screen_shot.delay(self.url, image_dir, self.image_path)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.url


@receiver(post_delete, sender=Site)
def remove_file(sender, instance, *args, **kwargs):
    file_path = os.path.join(
        settings.MEDIA_ROOT, os.path.join(instance.user.username, instance.image_path)
    )
    if os.path.exists(file_path):
        os.remove(file_path)


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
    image_dir = os.path.join(settings.MEDIA_ROOT, "users", username)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir
