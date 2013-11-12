from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from confsessions.models import Session, SessionTime
from confsessions.views import register_session

from userena.models import UserenaBaseProfile
from userena.models import UserenaSignup
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
            u.get_profile().set_paid()
    
    def __unicode__(self):
        return self.email

class Profile(UserenaBaseProfile):
    """ Default profile """
    GENDER_CHOICES = (
        (1, _('Male')),
        (0, _('Female')),
        (-1, _('Prefer not to identify')),
    )

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


    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile') 

    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    birth_date = models.DateField(_('birth date (yyyy-mm-dd)'), blank=True, null=True)
    affiliation = models.CharField(_('affiliation'), blank=True, null=True, max_length=25,
            choices=AFFIL_CHOICES, default=UBC_STUDENT)
    affil_other = models.CharField(_('other (if Other BC University or Other)'), blank=True, null=True, max_length=50)
    student_num = models.CharField(_('student number'), blank=True, null=True, max_length=8)
    phone_num = models.CharField(_('phone number'), blank=True, null=True, max_length=15)
    year_of_study = models.CharField(_('year of study'), blank=True, null=True, max_length=2,
            choices=YEAR_CHOICES, default='U1')
    faculty = models.CharField(_('faculty'),blank=True, null=True, max_length=50,
            choices = FACULTY_CHOICES)
    major = models.CharField(_('major/Specialization'), blank=True, null=True, max_length=50)
    vegan = models.BooleanField(_('are you vegan?'))
    vegetarian = models.BooleanField(_('are you vegetarian?'))
    diet = models.CharField(_('other dietary requirements:'), blank=True, null=True, max_length=25)
    times_participation = models.IntegerField(_('how many times have you participated in the SLC, including this year?'), blank=True, null=True)
    hear = models.ManyToManyField(HearAbout, verbose_name=_('How did you head about the Student Leadership Conference?'), blank=True, null=True)
    saved_sessions = models.ManyToManyField(Session)
    paid = models.BooleanField()

    def is_fully_registered(self):
        return self.get_registered_sessions().count() == SessionTime.objects.all().count()

    def get_saved_sessions(self):
        return self.saved_sessions.order_by('sessiontype__session_time__time')

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

    def readyForPayment(self):
        '''Checks all compulsory fields are filled for payment'''
        if len(self.user.first_name) < 2:
            return False 
        if len(self.user.last_name) < 2:
            return False 
        if self.affiliation == UBC_STUDENT:
            if len(self.student_num) < 8:
                return False
        return True

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
        return self.user.email 

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
        self.register_saved_sessions()
        self.save()

    def check_payment_groups(self):
        if self.has_group():
            self.set_paid()

    def has_group(self):
        u = User.objects.get(pk=self.user.pk)
        groups = PaymentGroupEmail.objects.filter(email=u.email)
        return groups.count() > 0
