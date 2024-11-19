from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Additional fields
    username = models.CharField(max_length=150, unique=True, null=True)  # Username field
    email = models.EmailField(null=True, blank=True)  # Email field
    password = models.CharField(max_length=128, null=True, blank=True)  # Password field, store hashed password only
    bio = models.TextField(blank=True, null=True)  # Add a bio field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Add a profile picture field

    def __str__(self):
        return self.username


class Poster(models.Model):
    
    username = models.CharField(max_length=150, unique=True, null=True)  # Username field
    password = models.CharField(max_length=128, null=True, blank=True)  # Password field, store hashed password only

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash the password
    

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Verify the hashed password