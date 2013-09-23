from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

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

class PaymentGroups(models.Model):
    payment_group = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    primary_group = models.BooleanField()
    def __unicode__(self):
        return self.payment_group + ":" + self.email


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

    #prefName = models.CharField(_('preferred name'), blank=True, null=True, max_length=30)
    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    #website = models.URLField(_('website'), blank=True, verify_exists=True, null=True)
    birth_date = models.DateField(_('birth date (yyyy-mm-dd)'), blank=True, null=True)
    affiliation = models.CharField(_('affiliation'), blank=True, null=True, max_length=25,
            choices=AFFIL_CHOICES, default=UBC_STUDENT)
    affil_other = models.CharField(_('other (if Other BC University or Other)'), blank=True, null=True, max_length=50)
    student_num = models.CharField(_('student number'), blank=True, null=True, max_length=8)
    phone_num = models.CharField(_('phone number'), blank=True, null=True, max_length=15)
    #address = models.TextField(_('address'), blank=True)
    year_of_study = models.CharField(_('year of study'), blank=True, null=True, max_length=2,
            choices=YEAR_CHOICES, default='U1')
    faculty = models.CharField(_('faculty'),blank=True, null=True, max_length=50,
            choices = FACULTY_CHOICES)
    other_faculty = models.CharField(_('other (if Faculty not listed)'), blank=True, null=True, max_length=50)
    major = models.CharField(_('major/Specialization'), blank=True, null=True, max_length=50)
    graduating = models.BooleanField(_('are you graduating this year?'))
    nut_allergy = models.BooleanField(_('are you allergic to nuts?'))
    vegan = models.BooleanField(_('are you vegan?'))
    vegetarian = models.BooleanField(_('are you vegetarian?'))
    gluten = models.BooleanField(_('are you gluten intolerant?'))
    lactose = models.BooleanField(_('are you lactose intolerant?'))
    diet = models.CharField(_('other dietary requirements:'), blank=True, null=True, max_length=25)
    times_participation = models.IntegerField(_('how many times have you participated in the SLC, including this year?'), blank=True, null=True)
    #hear_about = models.CharField(_('how did you hear about the SLC?'), blank=True, null=True, max_length=25,
    #        choices=HEAR_ABOUT_CHOICES)
    hear = models.ManyToManyField(HearAbout, blank=True, null=True)
    other = models.TextField(_('dear future self...'), blank=True, default='Maybe try setting a goal...')

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
        
    def unpaid(self):
        '''Checks if user is unpaid'''
        u = User.objects.get(pk=self.user.pk)
        user = UserenaSignup.objects.get(user=u)
        if user.is_paid():
            return False
        return True

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

    def has_group(self):
        u = User.objects.get(pk=self.user.pk)
        groups = PaymentGroups.objects.filter(email=u.email)
        if groups.count() > 0:
            return True
        return False

    def groups(self):
        u = User.objects.get(pk=self.user.pk)
        groups = PaymentGroups.objects.filter(email=u.email)
        return groups

    @property
    def age(self):
        if not self.birth_date: return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not a
            # leap year.
            try:
                birthday = self.birth_date.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = self.birth_date.replace(year=today.year, day=day)
            if birthday > today: return today.year - self.birth_date.year - 1
            else: return today.year - self.birth_date.year
