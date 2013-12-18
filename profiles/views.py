import csv
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from confsessions.models import Session, SessionTime
from confsessions.views import get_completed_session_times
from profiles.models import Profile, PaymentGroupEmail, PaymentGroup

from django.contrib.auth.models import User

def save_session(request, session_pk, user_pk):
    session = Session.objects.get(pk=session_pk)
    user = User.objects.get(pk=user_pk)
    user.profile.save_session(session)
    user.save()
    return HttpResponse('Success')

def review(request):
    if not request.user.is_authenticated():
        return redirect(reverse('userena_signin'))

    session_times = SessionTime.objects.all()
    context = { \
        'session_times' : session_times, \
        'completed_session_times' : get_completed_session_times(request.user), \
        'prev_sessiontime' : session_times[session_times.count() - 1], \
        'profile' : request.user.get_profile, \
        'is_review' : True, \
    }
    context['payment_groups'] = request.user.get_profile().get_payment_groups()
    return render(request, 'profiles/review.html', context)

def signin_success(request, username):
    profile = request.user.get_profile()
    if profile.paid:
        if profile.submitted_registration:
            return redirect('/accounts/review');
        else:
            return redirect('/sessions/')
    elif profile.is_ready_for_registration():
        return redirect('/sessions/')
    else:
        return redirect('/accounts/' + username + '/edit')

def registration_complete(request):
    if not request.user.is_authenticated():
        raise Http404

    profile = request.user.get_profile()

    if not profile.paid or profile.submitted_registration:
        raise Http404

    profile.submit_registration()
    profile.send_registration_confirmation_email()
    return render(request, 'profiles/payment_success.html')

def delegate_list(request):
    if not request.user.is_authenticated():
        raise Http404

    profile = request.user.get_profile()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="delegates.csv"'

    writer = csv.writer(response)
    writer.writerow([
    'Username',
    'First Name', 
    'Last Name',
    'Email',
    'Date Joined',
    'Affiliation', 
    'Affil other', 
    'Student Number',
    'Phone Number',
    'Year of Study',
    'Faculty',
    'Major',
    'Vegan?',
    'Vegetarian?',
    'Gluten free?',
    'Lactose Intolerant',
    'Diet',
    'Hear About',
    'Times Participated',
    'Paid',
    'Submitted Registration',
    'Opening',
    'Opening Time',
    'Opening Presenter',
    'Opening Location',
    'Featured Presenter 1',
    'Featured Presenter 1 Time',
    'Featured Presenter 1 Presenter',
    'Featured Presenter 1 Location',
    'Session 1',
    'Session 1 Time',
    'Session 1 Presenter',
    'Session 1 Location',
    'Lunch',
    'Lunch Time',
    'Lunch Presenter',
    'Lunch Location',
    'Session 2',
    'Session 2 Time',
    'Session 2 Presenter',
    'Session 2 Location',
    'Featured Presenter 2',
    'Featured Presenter 2 Time',
    'Featured Presenter 2 Presenter',
    'Featured Presenter 2 Location',
    'Closing',
    'Closing Time',
    'Closing Presenter',
    'Closing Location',
    ])
    profiles = Profile.objects.all()
    for profile in profiles:
        opening = profile.get_registered_session(0)
        fp1 = profile.get_registered_session(1)
        sess1 = profile.get_registered_session(2)
        lunch =profile.get_registered_session(3)
        sess2 =profile.get_registered_session(4)
        fp2 =profile.get_registered_session(5)
        closing =profile.get_registered_session(6)
        writer.writerow([
        profile.user.username,
        profile.user.first_name, 
        profile.user.last_name, 
        profile.user.email,
        profile.user.date_joined,
        profile.affiliation,
        profile.affil_other,
        profile.student_num,
        profile.phone_num,
        profile.year_of_study,
        profile.faculty,
        profile.major,
        profile.vegan,
        profile.vegetarian,
        profile.gluten_free,
        profile.lactose_intolerant,
        profile.diet,
        profile.get_hear_abouts(),
        profile.times_participation,
        profile.paid,
        profile.submitted_registration,
        opening,
        opening.get_time(),
        opening.presenter,
        opening.location,
        fp1,
        fp2.get_time(),
        fp1.presenter,
        fp1.location,
        sess1,
        sess1.get_time(),
        sess1.presenter,
        sess1.location,
        lunch,
        lunch.get_time(),
        lunch.presenter,
        lunch.location,
        sess2,
        sess2.get_time(),
        sess2.presenter,
        sess2.location,
        fp2,
        fp2.get_time(),
        fp2.presenter,
        fp2.location,
        closing,
        closing.get_time(),
        closing.presenter,
        closing.location,
        ])

    return response

@csrf_exempt
def payment_success(request):
    '''Redirect to payment success'''
    if request.POST.get('payment', 0):
        email = request.POST.get('cf_field_9', '')
        user = User.objects.get(email=email)
        payment_group = PaymentGroup.objects.get_or_create(name="Credit Card Payments", primary_group=False)[0]
        payment_group_email = PaymentGroupEmail.objects.get_or_create(email=email, payment_group=payment_group)
        payment_group.save()
        profile = user.get_profile()
        profile.set_paid()
        return render(request, 'profiles/payment_success.html')
    raise Http404
