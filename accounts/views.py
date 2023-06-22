from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm


class CustomLoginView(views.LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(views.LogoutView):
    pass


class CustomSignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("accounts:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "accounts/profile.html", context)


class CustomPasswordChangeView(views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
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
