from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Profile
from .forms import UserLoginForm, RegstrationForm, ProfileEditForm, UserEditForm, PasswordChangeForm


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data["username_or_email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username_or_email, password=password)

            if not user:
                try:
                    user = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                
                messages.success(request, "Zalogowano pomyślnie!")

                next_url = request.GET.get("next")

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse("main:home"))
            else:
                messages.error(request, "Niepoprawne dane logowania.")
    else:
        form = UserLoginForm()

    return render(request, "users/user_login.html", {
        "form": form
    })



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Wylogowano pomyślnie.")
    else:
        messages.warning(request, "Nie jesteś zalogowany.")

    return redirect(reverse("main:home"))


def user_register(request):
    if request.method == "POST":
        form = RegstrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)

            login(request, user)

            messages.success(request, "Rejestracja przebiegła pomyślnie.")
            
            return redirect("main:home")
        else:
            messages.error(request, "Wystąpił błąd podczas rejestracji.")
    else:
        form = RegstrationForm()

    return render(request, "users/user_register.html", {
        "form": form
    })


@login_required()
def edit_user(request):
    user = request.user
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Zapisano zmienione dane Twojego konta.")

            return redirect("users:edit_user")
        else:
            messages.error(request, "Wystąpił błąd podczas zapisu danych Twojego konta.")
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, "users/edit_user.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


@login_required()
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Twoje hasło zostało zmienione!")

            return redirect("users:change_password")
        else:
            messages.error(request, "Wystąpił błąd podczas zmiany hasła.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {
        "form": form
    })
