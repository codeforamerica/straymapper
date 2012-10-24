from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^animals/', include('animals.urls')),
    url(r'^report/',  include('reports.urls')),

    url(r'^$', 'animals.views.index', name='home'),
)
