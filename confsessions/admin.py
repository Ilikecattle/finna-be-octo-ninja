from django.contrib import admin
from confsessions.models import SessionTime, SessionType, Session

admin.site.register(SessionTime)
admin.site.register(SessionType)
admin.site.register(Session)
