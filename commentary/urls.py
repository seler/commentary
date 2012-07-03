from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'comm.views.home', name='home'),
    url(r'^new/$', 'comm.views.create_comm', name='create_comm'),
    url(r'^bupdate/(?P<pk>\d+)/$', 'comm.views.bupdate_comm', name='bupdate_comm'),
    url(r'^aupdate/(?P<pk>\d+)/$', 'comm.views.aupdate_comm', name='aupdate_comm'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
