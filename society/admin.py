from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Member

# Use get_user_model() to avoid issues with custom user registration
User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'flat_number', 'role', 'email')
    search_fields = ('user__username', 'email', 'phone_number')

# Register CustomUser only once
admin.site.register(User, CustomUserAdmin)

# Register the Member model
admin.site.register(Member, MemberAdmin)