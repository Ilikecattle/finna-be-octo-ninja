from django.conf.urls.defaults import *
from django.conf.urls import patterns, url

from profiles.forms import EditProfileFormExtra, SignupFormCrispy, SignInForm
from profiles import views

urlpatterns = patterns('',
    url(r'^signup/$', 'userena.views.signup', { 'signup_form' : SignupFormCrispy }, name='userena_signup'),
    url(r'^signin/$', 'userena.views.signin', { 'auth_form' : SignInForm }, name='userena_signin'),
    url(r'^(?P<username>[\.\w-]+)/edit/$', 'userena.views.profile_edit', {'edit_profile_form' : EditProfileFormExtra}, name='edit-profile'),

    # Payment
    url(r'^paymentsuccess/$', views.payment_success, name='payment_success'),
    url(r'^unpay/$', views.unpay, name='unpay'),

    url(r'^save_session/(\d*)/(\d*)/$', views.save_session, name='save_session'),

    url(r'^review/$', views.review, name='profiles_review'),

    url(r'^', include('userena.urls')),
    )
