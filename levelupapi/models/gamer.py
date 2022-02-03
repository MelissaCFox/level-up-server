from django.db import models
from django.contrib.auth.models import User


class Gamer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="attendees")
    bio = models.CharField(max_length=50)
