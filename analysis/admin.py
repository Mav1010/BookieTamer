from django.contrib import admin
from analysis.models import *


class MatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, MatchAdmin)
admin.site.register(Division, MatchAdmin)

