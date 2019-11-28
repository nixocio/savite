from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Category


@receiver(post_save, sender=User)
def init_new_user(instance, created, **kwargs):
    if created:
        print("post_save was called")
        categories = [
            "Back-End",
            "Business",
            "Career",
            "Economy",
            "Education",
            "Front-End",
            "JavaScript",
            "Linux",
            "Music",
            "Must Read",
            "Open Source",
            "Podcast",
            "Productivity",
            "Python",
            "Start-Up",
            "Web",
        ]
        for category in categories:
            Category.objects.create(name=category, user=instance)
            instance.category.save()
