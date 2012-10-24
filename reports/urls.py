from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'reports.views',
    url(r'^view/(?P<id>.*?)/$', 'view', name='reports_view'),
    url(r'^$', 'index', name='reports_index')
)
