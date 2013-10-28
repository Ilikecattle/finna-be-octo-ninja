from django.contrib import admin

from userena.utils import get_profile_model

from csvexport.admin import CSVAdmin
from profiles.models import HearAbout, PaymentGroup, PaymentGroupEmail, Profile

admin.site.unregister(get_profile_model())

class ProfileAdmin(CSVAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'paid']
    list_display_links = ['user']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

class PaymentGroupEmailAdmin(CSVAdmin):
    list_display = ['email']
    search_fields = ['email']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(HearAbout)
admin.site.register(PaymentGroup)
admin.site.register(PaymentGroupEmail, PaymentGroupEmailAdmin)
