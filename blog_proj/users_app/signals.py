# Django signals that allow create user profile when new user account is created.
from django.db.models.signals import post_save # signal which is fired after an object is saved, signal will be fired when we save new user
from django.contrib.auth.models import User # User model is a sender - something what is sending the signal
from django.dispatch import receiver # receiver is a function that get the signal and then perform some tasks
from .models import Profile

# this function will be run every time when new user will be created
@receiver(post_save, sender=User) # receiver is a decorator which takes 2 arguments - signal and sender (in this case post_save and User model)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# function that save new created profile
@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# WE HAVE TO REMEMBER ABOUT IMPORT SIGNALS IN APP CONFIG BY CREATING READY FUNCTION (in apps.py file)