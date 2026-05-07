from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProviderProfile, LearnerProfile, PasswordRecoveryRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_provider_verified', 'is_suspended', 'is_staff')
    list_filter = ('role', 'is_provider_verified', 'is_suspended', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': (
                'role', 'division', 'city', 'area', 'address', 'phone',
                'profile_picture', 'is_provider_verified', 'is_suspended', 'temporary_password_sent'
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {
            'fields': ('email', 'role')
        }),
    )
    ordering = ('email',)


admin.site.register(ProviderProfile)
admin.site.register(LearnerProfile)
admin.site.register(PasswordRecoveryRequest)