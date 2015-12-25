'''
Created on May 24, 2015

@author: luodichen
'''

from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'pages.views.info'),
    url(r'^login/$', 'pages.views.login'),
    url(r'^info/$', 'pages.views.info'),
    url(r'^report/$', 'pages.views.report'),
]
