from django.conf.urls.defaults import *
import settings
from accounts.views import *
from survey.views import *

handler500 = 'djangotoolbox.errorviews.server_error'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^home/$', home, name='home'),
    url(r'^accounts/signin/$', signin, name='signin'),
    url(r'^accounts/signup/$', signup, name='signup'),
    url(r'^accounts/signout/$', signout, name='signout'),
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^about/$', about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('survey.urls')),
    url(r'', include('social_auth.urls')),
) 

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
