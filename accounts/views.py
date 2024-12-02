from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("blog:index")
        else:
            messages.error(request, "Invalid username or email, or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form, "title": "Login"})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")
            user.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )

            # Send email notification
            # subject = "Welcome to Our Site"
            # message = f"Hello {username},\n\nThank you for registering on our site!"
            # from_email = settings.DEFAULT_FROM_EMAIL
            # recipient_list = [email]
            # send_mail(subject, message, from_email, recipient_list)

            return redirect("accounts:login")
        else:
            if "captcha" in form.errors:
                messages.error(request, "Invalid CAPTCHA. Please try again.")
            else:
                messages.error(
                    request, "Registration failed. Please correct the errors below."
                )
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form, "title": "Register"})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("blog:index")


def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name="password_reset_email.html",
                subject_template_name="password_reset_subject.txt",
                from_email=None,
                html_email_template_name=None,
            )
            messages.success(
                request,
                "An email has been sent with instructions to reset your password.",
            )
            return redirect("accounts:password_reset_done")
        else:
            messages.error(request, "Invalid username or email.")
    else:
        form = PasswordResetForm()
    return render(
        request, "forgot_password.html", {"form": form, "title": "Forgot password"}
    )


class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("blog:index")
    else:
        user_form = UserForm(instance=user)

    return render(
        request,
        "profile.html",
        {
            "user_form": user_form,
        },
    )
