# Django signals that allow create user profile when new user account is created.
from django.db.models.signals import post_save # signal which is fired after an object is saved (after saving new user)
from django.contrib.auth.models import User # sender - send signal
from django.dispatch import receiver # receiver - function which get the signal and then perform some tasks
from .models import Profile

# function run every time when new user is created
@receiver(post_save, sender=User) # receiver takes 2 arguments - signal and sender 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save new created profile
@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# IMPORT SIGNALS IN APP CONFIG - READY FUNCTION in apps.py 