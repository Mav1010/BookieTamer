from django.urls import path

from . import views


app_name = 'datafetch'

urlpatterns = [
    path('games-to-bet/', views.games_to_bet_list, name="games_to_bet"),
    path('settings/', views.DataFetchSettingsCreateView.as_view(), name="datafetch_settings_create"),
    path('settings/<int:pk>', views.DataFetchSettingsUpdateView.as_view(), name="datafetch_settings"),
]