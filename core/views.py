from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from users.forms import CustomUserChangeForm, CustomUserCreationForm


def home(request):
    User = get_user_model()
    count = User.objects.count()
    return render(request, "home.html", {"count": count})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

