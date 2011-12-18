from django.contrib import admin
from survey.models import *

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class PollInline(admin.StackedInline):
    model = Poll
    extra = 3

class SurveyAdmin(admin.ModelAdmin):
    inlines = [PollInline]

class VoteAdmin(admin.ModelAdmin):
    model = Vote

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)