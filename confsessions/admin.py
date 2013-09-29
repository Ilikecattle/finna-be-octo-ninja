from django.contrib import admin
from confsessions.models import SessionType, Session

admin.site.register(SessionType)
admin.site.register(Session)
