from django.http import HttpResponse
from django.shortcuts import render

from confsessions.models import SessionType, Session
from django.contrib.auth.models import User

def index(request):
    sessiontimes = SessionType.objects.all()
    context = {'sessiontimes': sessiontimes}
    return render(request, 'confsessions/sessions.html', context)

def sessiontype(request, sessiontype_pk):
    cur_session_type = SessionType.objects.get(pk=sessiontype_pk)
    sessiontypes = SessionType.objects.filter(include_in_nav=True).order_by('time')
    prev_sessiontype = None
    next_sessiontype = None
    save_next = False
    for s in sessiontypes:
        if save_next:
            next_sessiontype = s
            break
        if s == cur_session_type:
            save_next = True
        else:
            prev_sessiontype = s
    context = {'sessiontypes' : sessiontypes, 'sessiontype' : cur_session_type, 'next_sessiontype' : next_sessiontype, 'prev_sessiontype' : prev_sessiontype}
    return render(request, 'confsessions/sessiontype.html', context)

def concurrent(request):
    sessiontimes = SessionType.objects.all()
    context = {'sessiontimes': sessiontimes}
    return render(request, 'confsessions/sessionsadmin.html', context)

def concurrent_delegates(request, session_pk):
    sess = Session.objects.get(pk=session_pk)
    context = {'sessionparticipants': sess.participants.all()}
    return render(request, 'confsessions/sessiondelegates.html', context)

def register_session(request, session_pk, user_pk):
    '''Register user in session'''
    sess = Session.objects.get(pk=session_pk)
    sess.add_participant(User.objects.get(pk=user_pk))
    sess.save()
    return HttpResponse('Success')
