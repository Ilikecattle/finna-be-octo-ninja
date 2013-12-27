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
                if user in sess.participants.all():
                    return True
        return False
    
    def get_time(self):
        return self.time.strftime('%l:%M %p')
    
    def has_multiple_session_types(self):
        return self.sessiontype_set.all().count() > 1

    def __unicode__(self):
        return self.name

class SessionType(models.Model):
    session_time = models.ForeignKey(SessionTime, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    use_search_bar = models.BooleanField(default=False)
    
    def get_time(self):
        if hasattr(self, 'session_time') and self.session_time is not None:
            return self.session_time.get_time()
        return "No Time"
    
    def __unicode__(self):
        return self.name

class Session(models.Model):
    sessiontype = models.ForeignKey(SessionType)
    name = models.CharField(max_length=200)
    presenter = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(blank=True)
    teaser = models.CharField(max_length=2000, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    participants = models.ManyToManyField(User, blank=True)
    def add_participant(self,User):
        for sess_type in self.sessiontype.session_time.sessiontype_set.all():
            for sess in sess_type.session_set.all():
                sess.participants.remove(User)
        self.participants.add(User)

    def has_spaces(self):
        return self.capacity - self.participants.count() > 0
    
    def registered_delegates(self):
        return str(self.participants.count())

    def get_time(self):
        if hasattr(self, 'sessiontype'):
            return self.sessiontype.get_time()
        return "No Time"

    def __unicode__(self):
        return self.name
