from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# Create your models here.
# Define a custom User model named Account that inherits from AbstractUser
class Account(AbstractUser):
# Add a boolean field to indicate if the user is an event organizer
    is_event_organizer = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Check if the password is set and not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)