from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Import from Project
from accounts.manager import CustomUserManager


# Create your models here.
def phone_regex_validator():
    return RegexValidator(
        regex=r"^\+?1?\d{6,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=False, unique=True)
    is_vendor = models.BooleanField(null=False, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.email}"
