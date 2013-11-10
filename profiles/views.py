from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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

def view_schedule(request, username):
    extra_context = dict()
    extra_context['profile'] = request.user.get_profile()
    return render(request, 'profiles/view_schedule.html', extra_context)

def review(request):
    session_times = SessionTime.objects.all()
    context = { \
        'session_times' : session_times, \
        'completed_session_times' : get_completed_session_times(request.user), \
        'prev_sessiontime' : session_times[0] \
    }
    return render(request, 'profiles/review.html', context)

def signin_success(request, username):
    if request.user.get_profile().readyForPayment():
        return redirect('/sessions/')
    else:
        return redirect('/accounts/' + username + '/edit')

@csrf_exempt
def payment_success(request):
    '''Redirect to payment success'''
    user = request.user
    if user.is_authenticated():
        user.get_profile().set_paid()
        return render(request, 'profiles/payment_success.html')
    else:
        return HttpResponse('Hacker')

def unpay(request):
    user = request.user
    user.get_profile().paid = False
    user.get_profile().save()
    return HttpResponse('Success')
