from django.db import models
from django.contrib.auth.models import User
from django import forms
import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    website = models.URLField("Website", blank=True)
    gravatar = models.URLField("Gravatar", blank=True)
    twitter = models.CharField("Twitter", max_length=30)
    github = models.CharField("Github", max_length=30)
                    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Friendship(models.Model):
    RELATIONSHIP_STATUS = (
    (u'requested', u'Requested'),
    (u'mutual', u'Mutual')
    )
    user_a = models.ForeignKey(User, related_name='friendship_requester')
    user_b = models.ForeignKey(User, related_name='friendship_target')
    requested_date = models.DateTimeField('requested_date')
    accepted_date = models.DateTimeField('accepted_date')
    status = models.CharField(max_length=20, choices=RELATIONSHIP_STATUS)
        
    
                
    