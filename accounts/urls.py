from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    EditUserProfileView,
    ResetPasswordView,
    ChangePasswordView,
)

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("profile", UserProfileView.as_view()),
    path("editprofile", EditUserProfileView.as_view()),
    path("resetpassword", ResetPasswordView.as_view()),
    path("changepassword", ChangePasswordView.as_view()),
]
