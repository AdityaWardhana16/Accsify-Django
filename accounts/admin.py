from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','is_staff','is_admin','is_pelanggan','birthdate')
    list_filter = ('is_staff', 'is_admin', 'is_pelanggan', 'jenis_kelamin')

    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'birthdate',
        'jenis_kelamin','image')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_pelanggan')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','first_name','last_name','birthdate'),
        }),
    )
    
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)