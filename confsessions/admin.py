from django.contrib import admin
from confsessions.models import SessionTime, SessionType, Session

class SessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'sessiontype', 'presenter', 'location', 'registered_delegates', 'capacity']
    search_fields = ['name', 'presenter', 'location']
    ordering = ['name']
    list_filter = ['sessiontype']

class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'session_time']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['session_time']

class SessionTimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'time']
    ordering = ['time', 'name']
    search_fields = ['name']
    list_editable = ['time']

admin.site.register(SessionTime, SessionTimeAdmin)
admin.site.register(SessionType, SessionTypeAdmin)
admin.site.register(Session, SessionAdmin)
