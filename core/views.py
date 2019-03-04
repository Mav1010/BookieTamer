from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    current_user = request.GET

    context = {
        'current_user': current_user
    }
    return render(request, 'core/pages/home.html', context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)
