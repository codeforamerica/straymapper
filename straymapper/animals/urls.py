from django.conf.urls import patterns, include, url

urlpatterns = patterns('animals.views',
    url(r'^$', 'index', name='animals_index')
)
