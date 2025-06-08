from django.contrib.auth import forms
from accounts.models import CustomUser


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "first_name", "last_name", "is_vendor")


class CustomUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "first_name", "last_name", "is_vendor")
