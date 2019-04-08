from django.urls import path

from . import views


app_name = 'datafetch'

urlpatterns = [
    path('games-to-bet/', views.games_to_bet_list, name="games_to_bet"),
    path('settings/create/', views.DataFetchSettingsCreate.as_view(), name="datafetch_settings_create"),
    path('settings/all/', views.DataFetchSettingsList.as_view(), name="datafetch_settings_list"),
    path('settings/<int:pk>', views.DataFetchSettingsUpdate.as_view(), name="datafetch_settings_update"),
]