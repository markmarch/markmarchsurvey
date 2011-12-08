from django.db import models
from django.contrib.auth.models import User
from django import forms

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    website = models.URLField("Website", blank=True)
    gravatar = models.URLField("Gravatar", blank=True)
    twitter = models.CharField("Twitter", max_length=30)
    github = models.CharField("Github", max_length=30)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
