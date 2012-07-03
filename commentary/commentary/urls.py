from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'comm.views.home', name='home'),
    url(r'^new/$', 'comm.views.new', name='new'),
    url(r'^response/(?P<object_id>\d+)/$', 'comm.views.response', name='response'),
    url(r'^admin/', include(admin.site.urls)),
)
