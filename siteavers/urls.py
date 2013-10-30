from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'engine.views.home_view', name='home'),
                       url(r'^(?P<lang>[a-z]{3})/$', 'engine.views.home_view', name='home'),
                       # url(r'^siteavers/', include('siteavers.foo.urls')),
                       url(r'^(?P<page>points)/', include('points.urls')),
                       url(r'^(?P<lang>[a-z]{3})/(?P<page>points)/', include('points.urls')),
                       

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^(?P<page>[a-z_]+)/$', 'engine.views.inner_text_view', name='inner_text'),
                       url(r'^(?P<lang>[a-z]{3})/(?P<page>[a-z_]+)/$', 'engine.views.inner_text_view', name='inner_text'),
                       # url(r'^siteavers/', include('siteavers.foo.urls')),
)
