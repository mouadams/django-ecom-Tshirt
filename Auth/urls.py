from django.urls import path
from .views import LoginPage,RegisterPage,LogoutPage



urlpatterns = [
    path("login/", LoginPage, name="Login"),
    path("register/", RegisterPage, name="Register"),
    path("logout/", LogoutPage, name="Logout")
]