from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'reports.views',
    #url(r'^view/(?P<aid>.*?)/$', 'view', name='reports_view'),
    url(r'^$', 'index', name='reports_index')
)
