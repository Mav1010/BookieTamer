from django.urls import path

from datafetch import views

urlpatterns = [
    path('games-to-bet/', views.games_to_bet_list, name="games_to_bet"),
]