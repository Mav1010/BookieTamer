from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('analysis.urls')),
    path('', include('datafetch.urls')),

    # in order to go to home if blank address
    path('', RedirectView.as_view(url='home')),
]
