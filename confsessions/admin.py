from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.db import models

from csvexport.admin import CSVAdmin
from confsessions.models import SessionTime, SessionType, Session

class SessionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SessionAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = admin.widgets.AdminTextareaWidget()

class SessionAdmin(CSVAdmin):
    list_display = ['name', 'sessiontype', 'presenter', 'location', 'registered_delegates', 'capacity']
    search_fields = ['name', 'presenter', 'location', 'description']
    ordering = ['name']
    list_filter = ['sessiontype']
    extra_csv_fields = ['teaser', 'description']
    filter_horizontal = ['participants', ]
    list_display_links = ['name', 'sessiontype']
    readonly_fields = ['participants']
    form = SessionAdminForm

class SessionTypeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SessionTypeAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = admin.widgets.AdminTextareaWidget()

class SessionTypeAdmin(CSVAdmin):
    list_display = ['name', 'session_time']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['session_time']
    list_display_links = ['name', 'session_time']
    form = SessionTypeAdminForm

class SessionTimeAdmin(CSVAdmin):
    list_display = ['name', 'time']
    ordering = ['time', 'name']
    search_fields = ['name']
    list_editable = ['time']

admin.site.register(SessionTime, SessionTimeAdmin)
admin.site.register(SessionType, SessionTypeAdmin)
admin.site.register(Session, SessionAdmin)
