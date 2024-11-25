from django.contrib.auth.models import User
from django.db import models



class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


