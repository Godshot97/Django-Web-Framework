from django.db import models
from django.contrib.auth.models import User
from PIL import Image # it is required to work on images


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # jeśli usuniemy usera zostanie usunięty również jego profile, ale gdy usuniemy profile nie zostanie usunięty user
    # dodanie do profilu zdjęcia
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') # aby móc dodać pole ze zdjęciem musimy zainstalować moduł Pillow


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path) # open image of current instance

        if img.height > 300 or img.width > 300: # check if image have to be resized
            output_size = (300,300) # definition of image size
            img.thumbnail(output_size) # resizing
            img.save(self.image.path) # overwriting of image in the same location 

