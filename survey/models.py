from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
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
    
    def is_expired(self):
        if self.expire_date is None:
            return False
        else:
            now = datetime.datetime.now()
            return now > self.expire_date

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
            return True
            # check if user is a friend
            # as_user_a = Friendship.objects.get(status='mutual', user_b=user)
            # if as_user_a is not None:
            #     return True
            # else:
            #     as_user_b = self.user.friendship_target.objects.get(status='mutual',user_a=user)
            #     return as_user_b is not None
    
    def comments(self):
        return Comment.objects.filter(survey__pk=self.pk)

class Poll(models.Model):
    """Poll model"""
    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length=100)

    def __unicode__(self):
        return self.question
    
    def choice_counts(self):
        return Choice.objects.filter(poll__pk=self.pk).count()
            
    def choices(self):
        return Choice.objects.filter(poll__pk=self.pk).order_by('pk')

    def total_votes(self):
        return Vote.objects.filter(poll__pk=self.pk).count()
    
    def vote(self, user, choice):
        # check if this user already voted on this question
        try:
            previous_vote = Vote.objects.get(poll=self, user=user)
            if previous_vote.choice == choice:
                return
            previous_vote.choice.decrease_vote()
            previous_vote.choice = choice
            choice.increase_vote()
            previous_vote.save()
        except Vote.DoesNotExist:
            vote = Vote(poll=self, user=user, choice=choice)
            vote.save()
            choice.increase_vote()
    
    def get_user_choice(self, user):
        return Vote.objects.filter(poll=self, user=user)
    
class Choice(models.Model):
    """Choice model"""
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice
        
    def decrease_vote(self):
        self.votes = self.votes - 1
        self.save()
    
    def increase_vote(self):
        self.votes = self.votes + 1
        self.save()

    def percentage(self):
        total = self.poll.total_votes()
        if total == 0:
            return 0
        return (self.votes/float(total))*100

class Vote(models.Model):
    """Vote model"""
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + " voted on " + self.poll.survey.name
        
class Comment(models.Model):
    """Comments on survye"""
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment 
