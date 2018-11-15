from django.urls import path

from analysis import views

urlpatterns = [
    path('data/', views.MatchList.as_view(), name="data"),
    path('ajax-get-teams-by-division/', views.ajax_get_teams_by_division, name="ajax_get_teams_by_division"),
]

