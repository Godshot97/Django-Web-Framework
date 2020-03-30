from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Account, Profile


@receiver(post_save, sender=Account)
def create_or_update_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
        print("Profile was created!")
    else:
        instance.profile.save()
        print("Profile updated!")

