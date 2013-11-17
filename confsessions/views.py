from django.http import HttpResponse
from django.shortcuts import render, redirect

from confsessions.models import SessionTime, SessionType, Session
from django.contrib.auth.models import User

def allow_registration(request):
    return request.user.get_profile().is_ready_for_registration()

def redirect_to_edit_profile(request):
    return redirect('/accounts/' + request.user.username + '/edit')

def index(request):
    if request.user.is_authenticated() and not allow_registration(request):
        return redirect_to_edit_profile(request)

    sessiontimes = get_session_times()
    return redirect('/sessions/sessiontime/' + str(sessiontimes[0].pk))

def sessiontime(request, session_time_pk):
    if request.user.is_authenticated() and not allow_registration(request):
        return redirect_to_edit_profile(request)

    session_time = SessionTime.objects.get(pk=session_time_pk)
    session_types = session_time.sessiontype_set.all()
    
    # If there is only 1 session type immediately go to it
    if session_time.has_multiple_session_types():
        return render(request, 'confsessions/sessiontime.html', get_context_for_session_time(request, session_time_pk))
    else:
        return redirect('/sessions/sessiontype/' + str(session_types[0].pk))

def sessiontype(request, session_type_pk):
    
    if request.user.is_authenticated() and not allow_registration(request):
        return redirect_to_edit_profile(request)

    return render(request, 'confsessions/sessiontype.html', get_context_for_session_type(request, session_type_pk))

def get_context_for_session_time(request, session_time_pk):
    cur_session_time = SessionTime.objects.get(pk=session_time_pk)
    prev_session_time = get_prev_session_time(cur_session_time)

    next_session_time = get_next_session_time(cur_session_time)
    session_times = get_session_times()
    session_types = cur_session_time.sessiontype_set.all()

    context = { \
        'session_times' : session_times, \
        'session_types' : session_types, \
        'session_time' : cur_session_time, \
        'next_sessiontime' : next_session_time, \
        'completed_session_times' : get_completed_session_times(request.user), \
        'prev_sessiontime' : prev_session_time \
    }
    return context

def get_context_for_session_type(request, session_type_pk):
    cur_session_type = SessionType.objects.get(pk=session_type_pk)
    cur_session_time = cur_session_type.session_time
    context = get_context_for_session_time(request, cur_session_time.pk)
    if cur_session_time.has_multiple_session_types():
        prev_session_time = cur_session_time
        context['prev_sessiontime'] = prev_session_time;
    context['sessiontype'] = cur_session_type
    return context


def register_session(request, session_pk, user_pk):
    '''Register user in session'''
    sess = Session.objects.get(pk=session_pk)
    sess.add_participant(User.objects.get(pk=user_pk))
    sess.save()
    return HttpResponse('Success')

def get_completed_session_times(user):
    if not user.is_authenticated():
        return None
    session_time_list = get_session_times()
    completed_sessions = []
    for sess_time in session_time_list:
        if user.get_profile().is_registered_or_saved_for_sess_time(sess_time):
            completed_sessions.append(sess_time)
    return completed_sessions

def get_session_times():
    return list(SessionTime.objects.all())

def get_prev_session_time(cur_sess_time):
    session_times = get_session_times()
    
    cur_index = session_times.index(cur_sess_time)
    if cur_index == 0:
        return
    return session_times[cur_index-1]

def get_next_session_time(cur_sess_time):
    session_times = get_session_times()
    cur_index = session_times.index(cur_sess_time)
    if cur_index >= len(session_times) - 1:
        return
    return session_times[cur_index+1]
