from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Category
from users.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def init_new_user(instance, created, **kwargs):
    if created:
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
            "Open Source",
            "Podcast",
            "Productivity",
            "Python",
            "Start-Up",
            "Web",
        ]
        for category in categories:
            Category.objects.create(name=category, user=instance)
