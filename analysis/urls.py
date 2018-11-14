from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView

from analysis import views


urlpatterns = [
    path('home/', views.home, name="home"),
    path('data/', views.MatchList.as_view(), name="data"),
    path('ajax-get-teams-by-division/', views.ajax_get_teams_by_division, name="ajax_get_teams_by_division"),
]
