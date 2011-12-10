from django.db import models
from django.contrib.auth.models import User
import datetime

class Survey(models.Model):
    """Survey model"""
    VISIBILITY_CHOICE = (
        (u'private', u'Private'),
        (u'public', u'Public')
    )
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    create_date = models.DateTimeField('date created')
    expire_date = models.DateTimeField('expiration date')
    popularity = models.IntegerField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICE)

    def __unicode__(self):
        return self.name
    
    def num_of_questions(self):
        return Poll.objects.filter(survey__pk=self.pk).count()

class Poll(models.Model):
    """Poll model"""
    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length=100)

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    """Choice model"""
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice


