from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def createUser(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
