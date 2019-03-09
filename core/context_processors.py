from django.conf import settings

from datafetch.models import DataFetchSettings


def core_context(request):
    user_settings = DataFetchSettings.objects.filter().exists()

    core_context = {
        'user_settings': user_settings
    }
    return core_context