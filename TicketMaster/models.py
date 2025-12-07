from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FavouriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=20, blank=True)
    images_url = models.URLField(blank=True)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.user.username})"