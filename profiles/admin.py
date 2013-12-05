from django.contrib import admin

from userena.utils import get_profile_model

from csvexport.admin import CSVAdmin
from profiles.models import HearAbout, PaymentGroup, PaymentGroupEmail, Profile

admin.site.unregister(get_profile_model())

class ProfileAdmin(CSVAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'paid', 'submitted_registration', 'affil_other']
    list_display_links = ['user']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    filter_horizontal = ['saved_sessions']
    readonly_fields = ['get_registered_sessions', 'email']
    list_filter = ['paid', 'submitted_registration']

class PaymentGroupEmailInline(admin.TabularInline):
    model = PaymentGroupEmail

class PaymentGroupEmailAdmin(CSVAdmin):
    list_display = ['payment_group', 'email']
    search_fields = ['email']
    list_filter = ['payment_group__name']

class PaymentGroupAdmin(CSVAdmin):
    list_display = ['name', 'primary_group']
    search_fields = ['name']
    list_filter = ['name']
    inlines = [ PaymentGroupEmailInline ]
    list_editable = ['primary_group']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(HearAbout)
admin.site.register(PaymentGroup, PaymentGroupAdmin)
admin.site.register(PaymentGroupEmail, PaymentGroupEmailAdmin)
