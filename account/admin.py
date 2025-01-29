from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Register your models here.

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id", "email","is_staff", "is_active", "date_joined", "last_login")
    list_filter = ("email", "is_staff", "is_active", "date_joined", "last_login")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    date_hierarchy = 'create_at'

admin.site.register(User, CustomUserAdmin)
