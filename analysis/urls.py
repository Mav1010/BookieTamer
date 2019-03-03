from django.urls import path

from . import views


app_name = 'analysis'

urlpatterns = [
    path('data/', views.MatchList.as_view(), name="data"),
    path('ajax-load-teams-by-division/', views.ajax_load_teams_by_division, name="ajax-load-teams-by-division"),

]

