from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form_input"}),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput()
        }
