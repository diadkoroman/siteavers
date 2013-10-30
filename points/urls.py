# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns=patterns('',
                     url(r'^$','points.views.points_home_view',name='points_home'),
                     url(r'^ajx/cities/$','points.views.ajax_get_cities_list'),
)
