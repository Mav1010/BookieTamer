from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView

from analysis import views


urlpatterns = [
    path('home/', views.home, name="home")
]
