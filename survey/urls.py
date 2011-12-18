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
    url(r'^survey/(\d+)/question/edit/$', edit_question, name='edit_question'),
    # url(r'^login/(?P<backend>[^/]+)/$', auth, name='socialauth_begin'),
    # url(r'^complete/(?P<backend>[^/]+)/$', complete, name='socialauth_complete'),
    # url(r'^associate/(?P<backend>[^/]+)/$', associate, name='socialauth_associate_begin'),
    # url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
    #     name='socialauth_associate_complete'),
    # url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect, name='socialauth_disconnect'),
    # url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$', disconnect,
    #     name='socialauth_disconnect_individual'),
)
