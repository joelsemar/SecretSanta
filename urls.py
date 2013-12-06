from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.conf import settings
from main.models import Group

import consts
urlpatterns = patterns('',
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    (r'^submit/?$', 'main.views.submit'),
    (r'^admin/?', include(admin.site.urls)),
    (r'', 'main.views.home'),
)

