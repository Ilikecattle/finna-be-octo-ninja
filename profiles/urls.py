from django.conf.urls.defaults import *
from django.conf.urls import patterns, url

from profiles.forms import EditProfileFormExtra, SignupFormCrispy, SignInForm
from profiles import views

urlpatterns = patterns('',
    url(r'^register/complete$', views.registration_complete, name='registraton_complete'),

    url(r'^delegatelist/$', views.delegate_list, name='delegate_list'),

    # Payment
    url(r'^paymentsuccess/$', views.payment_success, name='payment_success'),
    
    url(r'^save_session/(\d*)/(\d*)/$', views.save_session, name='save_session'),
    
    url(r'^review/$', views.review, name='profiles_review'),
    
    url(r'^signup/$', 'userena.views.signup',
        { 'signup_form' : SignupFormCrispy },
        name='userena_signup'),
    url(r'^signin/$', 'userena.views.signin',
        { 'auth_form' : SignInForm },
        name='userena_signin'),
    url(r'^(?P<username>[\.\w-]+)/edit/$', 'userena.views.profile_edit',
        {'success_url' : '/sessions/', 'edit_profile_form' : EditProfileFormExtra},
        name='edit-profile'),
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
        views.signin_success, name='signin_success'),

    url(r'^', include('userena.urls')),
    )
