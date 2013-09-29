from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from confsessions import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='sessions'),
        url(r'^(\d*)', views.sessiontype),
        url(r'^concurrent/$', views.concurrent, name='concurrent'),
        url(r'^concurrent_delegates/(\d*)/$', views.concurrent_delegates, name='concurrent_delegates'),
        url(r'^register_session/(\d*)/(\d*)/$', views.register_session, name='register_session'),
        )
