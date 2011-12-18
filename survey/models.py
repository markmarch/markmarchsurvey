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
    create_date = models.DateTimeField('date created', auto_now_add=True)
    expire_date = models.DateTimeField('expiration date', null=True)
    popularity = models.IntegerField(default=0)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICE)

    def __unicode__(self):
        return self.name
    
    def num_of_questions(self):
        return Poll.objects.filter(survey__pk=self.pk).count()
        
    def polls(self):
        return Poll.objects.filter(survey__pk=self.pk)
        
    def belongs_to(self, user):
        return self.user.username==user.username
        
    def can_vote(self, user):
        if self.visibility == 'public' or self.user == user:
            return True
        else:
            # check if user is a friend
            as_user_a = self.user.friendship_requester.objects.get(status='mutual', user_b=user)
            if as_user_a is not None:
                return True
            else:
                as_user_b = self.user.friendship_target.objects.get(status='mutual',user_a=user)
                return as_user_b is not None
            

class Poll(models.Model):
    """Poll model"""
    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length=100)

    def __unicode__(self):
        return self.question
        
    def choices(self):
        return Choice.objects.filter(poll__pk=self.pk)
    

class Choice(models.Model):
    """Choice model"""
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice
        
class Vote(models.Model):
    """Vote model"""
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    choice = models.IntegerField()
    
    def __unicode__(self):
        return user.username + "voted on " + poll.survey.name
         


