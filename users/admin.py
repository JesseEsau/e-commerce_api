from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Display additional fields in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city', 'state', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city', 'state', 'phone', 'address')}),
    )


# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)
