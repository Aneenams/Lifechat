from django.contrib import admin
from lifeapp.models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'city', 'blood_status', 'badge_tier', 'verified_donation_count')
    list_filter = ('blood_group', 'city', 'blood_status', 'account_type')
    search_fields = ('user__username', 'user__email', 'city')