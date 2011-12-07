from django.conf.urls.defaults import *
import settings
from accounts.views import *

handler500 = 'djangotoolbox.errorviews.server_error'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^home/$', home, name='home'),
    url(r'^signout/$', signout, name='signout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
) 

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
