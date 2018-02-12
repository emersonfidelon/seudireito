from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserAdminCreationForm, UserAdminForm

class UserAdmin(BaseUserAdmin):
    
    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('name', 'username', 'email', 'password', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('name','email')
        }),
        ('Informações Básicas', {
            'fields': ('name', 'date_joined', 'last_login')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups','user_permissions'
                )
            }
        ),
    )
    list_display = ['name', 'email', 'is_active', 'is_staff', 'is_company', 'is_lawyer', 'date_joined']

admin.site.register(User, UserAdmin)
