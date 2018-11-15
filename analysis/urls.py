from django.urls import path

from analysis import views, filters

urlpatterns = [
    path('data/', views.MatchList.as_view(), name="data"),
]

