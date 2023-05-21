from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "username",
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
