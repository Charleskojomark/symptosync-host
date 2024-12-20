from django.contrib.auth.models import User
from django.db import models
from interactions.models import Post



class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(
        upload_to="profile_images",
        default="profile_img.jpeg",
    )
    follows = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )
    posts = models.ManyToManyField(Post, related_name="associated_profiles", blank=True)

    liked_posts = models.ManyToManyField(
        Post, related_name="liked_by_profiles", blank=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"
    

