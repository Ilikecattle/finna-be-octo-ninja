from django.http import HttpResponse
from django.shortcuts import render, redirect

from confsessions.models import SessionTime, SessionType, Session
from django.contrib.auth.models import User

def index(request):
    sessiontimes = get_session_times_ordered()
    return redirect('/sessions/sessiontime/' + str(sessiontimes[0].pk))

def sessiontime(request, session_time_pk):
    session_time = SessionTime.objects.get(pk=session_time_pk)
    session_types = session_time.sessiontype_set.all()
    
    # If there is only 1 session type immediately go to it
    if session_time.has_multiple_session_types():
        return render(request, 'confsessions/sessiontime.html', get_context_for_session_time(request, session_time_pk))
    else:
        return redirect('/sessions/sessiontype/' + str(session_types[0].pk))

def sessiontype(request, session_type_pk):
    return render(request, 'confsessions/sessiontype.html', get_context_for_session_type(request, session_type_pk))

def get_context_for_session_time(request, session_time_pk):
    cur_session_time = SessionTime.objects.get(pk=session_time_pk)

    if cur_session_time.has_multiple_session_types():
        prev_session_time = cur_session_time
    else:
        prev_session_time = get_prev_session_time(cur_session_time)

    next_session_time = get_next_session_time(cur_session_time)
    session_times = get_session_times_ordered()
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
    context = get_context_for_session_time(request, cur_session_type.session_time.pk)
    context['sessiontype'] = cur_session_type
    return context


def register_session(request, session_pk, user_pk):
    '''Register user in session'''
    sess = Session.objects.get(pk=session_pk)
    sess.add_participant(User.objects.get(pk=user_pk))
    sess.save()
    return HttpResponse('Success')

def get_completed_session_times(user):
    session_time_list = get_session_times_ordered()
    for sess_time in session_time_list:
        if not sess_time.is_user_registered(user):
            session_time_list.remove(sess_time)
    return session_time_list

def get_session_times_ordered():
    return list(SessionTime.objects.order_by('time'))

def get_prev_session_time(cur_sess_time):
    session_times = get_session_times_ordered()
    
    cur_index = session_times.index(cur_sess_time)
    if cur_index == 0:
        return
    return session_times[cur_index-1]

def get_next_session_time(cur_sess_time):
    session_times = get_session_times_ordered()
    cur_index = session_times.index(cur_sess_time)
    if cur_index >= len(session_times) - 1:
        return
    return session_times[cur_index+1]
