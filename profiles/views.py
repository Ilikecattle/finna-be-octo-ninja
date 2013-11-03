from django.http import HttpResponse
from django.shortcuts import render, redirect
from confsessions.models import Session, SessionTime
from confsessions.views import get_completed_session_times
from profiles.models import Profile

from django.contrib.auth.models import User

def save_session(request, session_pk, user_pk):
    session = Session.objects.get(pk=session_pk)
    user = User.objects.get(pk=user_pk)
    user.profile.save_session(session)
    user.save()
    return HttpResponse('Success')

def review(request):
    session_times = SessionTime.objects.all()
    context = { \
        'session_times' : session_times, \
        'completed_session_times' : get_completed_session_times(request.user), \
        'prev_sessiontime' : session_times[0] \
    }
    return render(request, 'profiles/review.html', context)

def payment(request, profile_pk):
    '''Change payment'''
    profile = Profile.objects.get(pk=profile_pk)
    profile.paid = True
    profile.register_saved_sessions()
    profile.save()
    return redirect('/accounts/paymentsuccess')

def payment_success(request):
    '''Redirect to payment success'''
    return render(request, 'profiles/payment_success.html')
