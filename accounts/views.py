from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


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
