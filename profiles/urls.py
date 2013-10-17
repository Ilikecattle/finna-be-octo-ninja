from django.conf.urls.defaults import *
from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^save_session/(\d*)/(\d*)/$', views.save_session, name='savesession')
    )
