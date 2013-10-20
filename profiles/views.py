from django.http import HttpResponse
from django.shortcuts import render
from confsessions.models import Session
from confsessions.views import get_session_times_ordered, get_completed_session_times

from django.contrib.auth.models import User

def save_session(request, session_pk, user_pk):
    session = Session.objects.get(pk=session_pk)
    user = User.objects.get(pk=user_pk)
    user.profile.save_session(session)
    user.save()
    return HttpResponse('Success')

def review(request):
    session_times = get_session_times_ordered()
    context = { \
        'session_times' : session_times, \
        'completed_session_times' : get_completed_session_times(request.user), \
        'prev_sessiontime' : session_times[-1] \
    }
    return render(request, 'profiles/review.html', context)
