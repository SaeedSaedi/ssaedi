from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("blog:index")
            else:
                messages.error(request, "Invalid username or email, or password.")
        else:
            messages.error(request, "Invalid username or email, or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")
            user.save()
            username = form.cleaned_data.get("username")
            # email = form.cleaned_data.get("email")
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
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


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
    return render(request, "forgot_password.html", {"form": form})


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
