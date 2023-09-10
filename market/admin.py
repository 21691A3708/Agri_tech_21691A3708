from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Production

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role_type')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role_type'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'seed_type', 'starting_date', 'crop_status', 'harvesting_date']
    list_filter = ['crop_name', 'seed_type', 'starting_date', 'crop_status', 'harvesting_date']
    search_fields = ['crop_name', 'seed_type', 'bio_of_crop']
