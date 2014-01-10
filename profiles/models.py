from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from confsessions.models import Session, SessionTime, SessionType
from confsessions.views import register_session

from userena import settings as userena_settings
from userena.models import UserenaBaseProfile
from userena.models import UserenaSignup
from userena.mail import send_mail
from userena.utils import get_protocol
import datetime

NOT_UBC = 'NotUBC'
UBC_STUDENT = 'UBCStudent'
UBC_STAFF = 'UBCStaff'
UBC_FACULTY = 'UBCFaculty'
UBC_ALUMNI = 'UBCAlumni'
HIGH_SCHOOL = 'High School'
OTHER_BC = 'Other BC University'
OTHER = 'Other'

class HearAbout(models.Model):
    description = models.CharField(_('how did you hear about the SLC?'), max_length=300)
    def __unicode__(self):
        return self.description

class PaymentGroup(models.Model):
    name = models.CharField(max_length=200)
    primary_group = models.BooleanField()
    def __unicode__(self):
        return self.name

class PaymentGroupEmail(models.Model):
    payment_group = models.ForeignKey(PaymentGroup)
    email = models.EmailField(max_length=250)
    
    def save(self, *args, **kwargs):
        super(PaymentGroupEmail, self).save(*args, **kwargs)
        users = User.objects.filter(email=self.email)
        for u in users:
            if u.is_authenticated():
                u.get_profile().set_paid()

    def __unicode__(self):
        return self.email

class Profile(UserenaBaseProfile):
    """ Default profile """

    AFFIL_CHOICES = (
        (UBC_STUDENT, 'UBC Student'),
        (UBC_FACULTY, 'UBC Faculty'),
        (UBC_STAFF, 'UBC Staff'),
        (UBC_ALUMNI, 'UBC Alumni'),
        (HIGH_SCHOOL, 'High School'),
        (OTHER_BC, 'Other BC University'),
        (OTHER, 'Other'),
        )

    YEAR_CHOICES = (
        ('U1', '1st Year'),
        ('U2', '2nd Year'),
        ('U3', '3rd Year'),
        ('U4', '4th Year'),
        ('U5', '5th Year+'),
        ('MA', 'Masters'),
        ('PD', 'PhD'),
        ('AL', 'Alumni'),
        ('ST', 'Staff'),
        ('HS', 'High School'),
        ('OT', 'Other'),
        )

    FACULTY_CHOICES = (
        ('Arts', 'Arts'),
        ('Dentistry','Dentistry'),
        ('Education','Education'),
        ('Engineering','Engineering'),
        ('Forestry','Forestry'),
        ('Kinesiology','Kinesiology'),
        ('Land and Food Systems','Land and Food Systems'),
        ('Music','Music'),
        ('Nursing','Nursing'),
        ('Sauder School of Business','Sauder School of Business'),
        ('Science','Science'),
        ('Other','Other'),
        )

    HEAR_ABOUT_CHOICES = (
        ('Our Website','Our Website'),
        ('Another UBC Website','Another UBC Website'),
        ('Education','Education'),
        ('Supervisor/Program Coordinator','Supervisor/Program Coordinator'),
        ('Facebook','Facebook'),
        ('Twitter','Twitter'),
        ('Community Release/Email','Community Release/Email'),
        ('Word of Mouth','Word of Mouth'),
        ('Residence','Residence'),
        ('Promotional Video','Promotional Video'),
        ('Promotional Materials','Promotional Materials'),
        ('Promotional Booth','Promotional Booth'),
        ('Classroom Announcements','Classroom Announcements'),
        )

    TIMES_PARTICIPATED_CHOICES = (
        zip(range(1,10), range(1, 10))
    )


    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile') 

    affiliation = models.CharField(_('affiliation'), null=True, max_length=25,
            choices=AFFIL_CHOICES, default=UBC_STUDENT)
    affil_other = models.CharField(_('other (if Other BC University or Other)'), blank=True, null=True, max_length=50)
    student_num = models.CharField(_('student number'), blank=True, null=True, max_length=8)
    phone_num = models.CharField(_('phone number'), null=True, max_length=15)
    year_of_study = models.CharField(_('year of study'), null=True, max_length=2,
            choices=YEAR_CHOICES)
    faculty = models.CharField(_('faculty'), null=True, max_length=50,
            choices = FACULTY_CHOICES)
    major = models.CharField(_('major/Specialization'), blank=True, null=True, max_length=50)
    vegan = models.BooleanField(_('vegan'))
    vegetarian = models.BooleanField(_('vegetarian'))
    gluten_free = models.BooleanField(_('gluten free'))
    lactose_intolerant = models.BooleanField(_('lactose intolerant'))
    diet = models.CharField(_('other dietary requirements:'), blank=True, null=True, max_length=25)
    times_participation = models.IntegerField(_('how many times have you participated in the SLC, including this year?'), null=True, choices=TIMES_PARTICIPATED_CHOICES)
    hear = models.ManyToManyField(HearAbout, verbose_name=_('How did you hear about the Student Leadership Conference?'), null=True)
    saved_sessions = models.ManyToManyField(Session)
    paid = models.BooleanField()
    submitted_registration = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.submitted_registration:
            for sess in self.saved_sessions.all():
                sess.add_participant(self.user)
                sess.save()
        super(Profile, self).save(*args, **kwargs)

    def is_registered_or_saved_for_sess_time(self, sess_time):
        if self.submitted_registration:
            return sess_time.is_user_registered(self.user)
        
        for session in self.saved_sessions.all():
            if session.sessiontype.session_time == sess_time:
                return True
        return False

    def get_saved_sessions(self):
        return self.saved_sessions.order_by('sessiontype__session_time__time')

    def get_registered_session(self, session_time_index):
        sessions = self.get_registered_sessions()
        if session_time_index < sessions.count():
            return sessions[session_time_index]
        else:
            return Session(name="No Session Found", sessiontype=SessionType(name="No Session Type", description="No desc"))

    def get_registered_sessions(self):
        return Session.objects.filter(participants__pk=self.user.pk).order_by('sessiontype__session_time__time')

    def save_session(self, session):
        for sess_type in session.sessiontype.session_time.sessiontype_set.all():
            for sess in sess_type.session_set.all():
                self.saved_sessions.remove(sess)
        self.saved_sessions.add(session)

    def register_saved_sessions(self):
        for sess in self.saved_sessions.all():
            sess.add_participant(self.user)
            sess.save()
        self.saved_sessions.clear()
        self.save()

    def is_ready_for_registration(self):
        '''Checks all compulsory fields are filled for payment'''
        if len(self.user.first_name) < 2 or len(self.user.last_name) < 2:
            return False 
        if self.affiliation == UBC_STUDENT:
            if len(self.student_num) < 8:
                return False
        return True

    def has_full_saved_session(self):
        for sess in self.saved_sessions.all():
            if not sess.has_spaces():
                return True
        return False

    def get_full_saved_sessions(self): 
        full_saved_sessions = []
        for sess in self.saved_sessions.all():
            if not sess.has_spaces():
                full_saved_sessions.append(sess.name)
        return ' & '.join([str(i) for i in full_saved_sessions])

    def is_ready_for_payment(self):
        return not self.has_full_saved_session() and self.get_saved_sessions().count() == SessionTime.objects.all().count()

    def get_user(self):
        return UserenaSignup.objects.get(user=self.user)

    def first_name(self):
        '''Getter for the first name for django admin'''
        return self.user.first_name
    first_name.admin_order_field = 'user__first_name'

    def last_name(self):
        '''Getter for the last name for django admin'''
        return self.user.last_name
    last_name.admin_order_field = 'user__last_name'

    def email(self):
        return self.user.email

    def is_student(self):
        '''Return 1 if student, else 0'''
        if self.affiliation == UBC_STUDENT:
            return "1"
        return "0"

    def is_ubc(self):
        '''Return 1 if UBC, else 0'''
        if self.affiliation in (UBC_STUDENT, UBC_STAFF, UBC_ALUMNI, UBC_FACULTY):
            return "1"
        return "0"

    def is_slc_email(self):
        '''Return if has slc email address'''
        if self.user.email.endswith('slc.ubc.ca'):
            return True
        return False

    def studentnum(self):
        '''Return 0 if not a student else student num'''
        if self.affiliation == UBC_STUDENT:
            return self.student_num
        return 0

    def phonenum(self):
        '''Return 0 if blank else return phone num'''
        if len(self.phone_num) < 2:
            return 0
        return self.phone_num

    def set_paid(self):
        self.paid = True
        self.save()

    def check_payment_groups(self):
        if self.paid:
            return
        if self.has_group():
            self.set_paid()

    def get_hear_abouts(self):
        result = []
        for h in self.hear.all():
            result.append(str(h))
        return ', '.join([i for i in result])

    def get_payment_groups(self):
        self.check_payment_groups()
        emails = PaymentGroupEmail.objects.filter(email=self.user.email)
        result = []
        for email in emails:
            result.append(email.payment_group)

        return ' & '.join([str(i) for i in result])

    def has_group(self):
        groups = PaymentGroupEmail.objects.filter(email=self.user.email)
        return groups.count() > 0

    def submit_registration(self):
        self.submitted_registration = True
        self.register_saved_sessions()
        self.save()

    def send_registration_confirmation_email(self):
        context = {'user': self.user,
                  'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES,
                  'protocol': get_protocol(),
                  'site': Site.objects.get_current()}

        subject = render_to_string('profiles/emails/registration_confirm_subject.txt',
                                       context)
        subject = ''.join(subject.splitlines())

        if (not userena_settings.USERENA_HTML_EMAIL or not message_old_html or
            userena_settings.USERENA_USE_PLAIN_TEMPLATE):
            message = render_to_string('profiles/emails/registration_confirm_message.txt',
                                       context)

        if self.user.email:
            send_mail(subject,
                      message,
                      None,
                      settings.DEFAULT_FROM_EMAIL,
                    [self.user.email])
