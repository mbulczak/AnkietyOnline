from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Profile


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Nazwa użytkownika lub e-mail")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło")

    class Meta:
        model = User


class RegstrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "date_of_birth", "phone_number"]
        widgets = {
            "date_of_birth": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control", 
                    "placeholder": "Wybierz date",
                    "type": "date"
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )
        }
