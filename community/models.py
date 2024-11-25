from django.db import models
from userauth.models import UserProfile


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(UserProfile, related_name='groups', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} - {self.group.name}"

