from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import reverse_lazy


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/passwordchange.html'
    success_url = reverse_lazy('users:passwordchangedone')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/passwordchangedone.html'


class SignInView(LoginView):
    template_name = 'users/signin.html'


class SignOutView(LogoutView):
    pass
