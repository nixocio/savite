from django.contrib.auth import get_user_model
from django.db import models


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
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    image_path = models.CharField(max_length=300)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=False)

    @property
    def image_path_modified(self):
        return 'default_image.jpg'
        
    #     @property
    # def hostname(self):
    #     return urlparse.urlparse(self.url).hostname


    class Meta:
        ordering = ("-modified_at",)

    def __str__(self):
        return "{}"
