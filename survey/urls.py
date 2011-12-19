"""URLs module"""
from django.conf.urls.defaults import patterns, url

from survey.views import *


urlpatterns = patterns('',
    url(r'^survey/(\d+)/$', survey, name='survey'),
    url(r'^survey/(\d+)/vote/$', vote, name='vote'),
    url(r'^survey/new/$', new, name='new'),
    url(r'^survey/(\d+)/question/add/$', add_question, name='add_question'),
    url(r'^survey/(\d+)/comment/$', comment, name='comment'),
    url(r'^survey/(\d+)/edit/$', edit, name='edit'),
    url(r'^survey/(\d+)/delete/$', delete, name='delete'),
    url(r'^survey/(\d+)/question/edit/$', edit_survey_questions, name='edit_survey_questions'),
    url(r'^survey/(\d+)/(\d+)/edit/$', edit_question, name='edit_question'),
    url(r'^survey/(\d+)/(\d+)/delete/$', delete_question, name='delete_question'),
)
