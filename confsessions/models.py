from datetime import datetime 
from django.db import models
from django.contrib.auth.models import User

class SessionTime(models.Model):
    time = models.TimeField(default=datetime.now(), null=True)
    name = models.CharField(max_length=30)
    
    class Meta:
        ordering = ('time',)
    
    def is_user_registered(self,user):
        if not user.is_authenticated():
            return False

        for sess_type in self.sessiontype_set.all():
            for sess in sess_type.session_set.all():
                if sess.participants.filter(pk=user.pk):
                    return True
        return False
    
    def has_multiple_session_types(self):
        return self.sessiontype_set.all().count() > 1

    def __unicode__(self):
        return self.name

class SessionType(models.Model):
    session_time = models.ForeignKey(SessionTime, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    def __unicode__(self):
        return self.name

class Session(models.Model):
    sessiontype = models.ForeignKey(SessionType)
    name = models.CharField(max_length=200)
    presenter = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    teaser = models.CharField(max_length=2000)
    description = models.CharField(max_length=5000)
    participants = models.ManyToManyField(User)
    def add_participant(self,User):
        for sess_type in self.sessiontype.session_time.sessiontype_set.all():
            for sess in sess_type.session_set.all():
                sess.participants.remove(User)
        self.participants.add(User)

    def has_spaces(self):
        spaces = self.capacity - self.participants.count()
        if spaces <=0:
            return False
        else: 
            return True
    
    def registered_delegates(self):
        return str(self.participants.count())

    def get_time(self):
        return self.sessiontype.session_time.time.strftime('%l:%M %p')

    def __unicode__(self):
        return self.name

'''class MySessions(models.Model):
    session = models.ForeignKey(Session)
    participant = models.ManyToManyField(User)
    def __unicode__(self):
        return self.session
        '''
