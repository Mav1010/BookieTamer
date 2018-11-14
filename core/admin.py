from django.contrib import admin
from core.models import *


class MatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, MatchAdmin)
admin.site.register(Division, MatchAdmin)

