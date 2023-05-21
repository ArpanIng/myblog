from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class CustomLoginView(views.LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(views.LogoutView):
    pass


class CustomSignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


class CustomPasswordChangeView(views.PasswordChangeView):
    template_name = "accounts/password_change_form.html"


class CustomPasswordChangeDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_change_done.html"


class CustomPasswordResetView(views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    template_name = "accounts/password_reset_form.html"


class CustomPasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class CustomPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
