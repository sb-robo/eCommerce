from django.urls import path
from .views import RegisterView, UserAccountView, LoginView

urlpatterns = [
    path("profile", UserAccountView.as_view()),
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
]
