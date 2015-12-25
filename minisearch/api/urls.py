'''
Created on May 23, 2015

@author: luodichen
'''
#from django.conf.urls import include
#from django.conf.urls.defaults import *

from django.conf.urls import url

urlpatterns = [
    url(r'^query/$', 'api.views.query'),
    url(r'login/$', 'api.views.login'),
    url(r'logout/$', 'api.views.logout'),
    url(r'report/$', 'api.views.report'),
]
