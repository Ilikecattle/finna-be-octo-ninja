from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from confsessions import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='sessions'),
        url(r'^sessiontime/(\d*)', views.sessiontime, name='sessiontime'),
        url(r'^sessiontype/(\d*)', views.sessiontype, name='sessiontype'),
        url(r'^register_session/(\d*)/(\d*)/$', views.register_session, name='register_session'),
        url(r'^sessionlist/$', views.delegate_list, name='sessionlist'),
        )
