from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )
    role_type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    age = models.PositiveIntegerField(blank=True, null=True)
    mobile = models.PositiveIntegerField(blank=True, null=True)
    city_village = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.username


class Production(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    seed_type = models.CharField(max_length=100)
    starting_date = models.DateField()
    crop_status = models.CharField(max_length=100)
    bio_of_crop = models.TextField()
    harvesting_date = models.DateField()
    image = models.ImageField(upload_to='productions/', null=True, blank=True)

    def __str__(self):
        return self.crop_name


User = get_user_model()
class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser)
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


