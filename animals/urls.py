from django.conf.urls import patterns, include, url

urlpatterns = patterns('animals.views',
    url(r'^messages/$', 'process_data', name='animals_process_data'),
    url(r'^view/(?P<aid>.*?)/$', 'view', name='animals_view'),
    url(r'^$', 'index', name='animals_index')
)
