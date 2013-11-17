from django.http import HttpResponse, Http404
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
        'prev_sessiontime' : session_times[session_times.count() - 1], \
        'profile' : request.user.get_profile, \
        'is_review' : True, \
    }
    return render(request, 'profiles/review.html', context)

def signin_success(request, username):
    profile = request.user.get_profile()
    if profile.paid:
        if profile.is_fully_registered():
            return redirect('/accounts/' + username + '/schedule');
        else:
            return redirect('/sessions/')
    elif profile.is_ready_for_registration():
        return redirect('/sessions/')
    else:
        return redirect('/accounts/' + username + '/edit')

@csrf_exempt
def payment_success(request):
    '''Redirect to payment success'''
    if request.POST.get('payment', 0):
        email = request.POST.get('cf_field_9', '')
        user = User.objects.get(email=email)
        profile = user.get_profile()
        profile.set_paid()
        return render(request, 'profiles/payment_success.html')
    raise Http404

def unpay(request):
    user = request.user
    user.get_profile().paid = False
    user.get_profile().save()
    return HttpResponse('Success')
