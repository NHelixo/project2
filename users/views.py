from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")
