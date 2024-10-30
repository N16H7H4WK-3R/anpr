from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

if not admin.site.is_registered(OutstandingToken):
    @admin.register(OutstandingToken)
    class OutstandingTokenAdmin(admin.ModelAdmin):
        list_display = ('user', 'jti', 'token_type', 'created', 'expires_at')
        search_fields = ('user__username', 'jti')

if not admin.site.is_registered(BlacklistedToken):
    @admin.register(BlacklistedToken)
    class BlacklistedTokenAdmin(admin.ModelAdmin):
        list_display = ('token', 'blacklisted_at')
        search_fields = ('token__user__username', 'token__jti')


class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the Django Admin interface
    list_display = ('username', 'role',
                    'last_login', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')

    # Define the fieldsets (sections) to display when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {
         'fields': ('role', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define fields that appear when creating a new user in the admin interface
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )

    ordering = ('username',)


# Register the custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
