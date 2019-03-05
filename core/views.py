from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):

    context = {
    }
    return render(request, 'core/pages/home.html', context)


