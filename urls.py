from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

from app.views import home, done, logout, error
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    # ('^$', 'django.views.generic.simple.direct_to_template',
    #  {'template': 'home.html'}),

    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)
