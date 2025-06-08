from django.contrib import admin, auth

from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(auth.admin.UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_vendor")

    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_vendor",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    # When creating a new user via the admin
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_vendor",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    ]

    ordering = [
        "email",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
