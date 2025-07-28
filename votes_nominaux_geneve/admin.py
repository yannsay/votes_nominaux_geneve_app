from django.contrib import admin
from .models import RSGETaxonomieData, RSGEVotingsData, otherVotingsData, votesData, personsData
# Register your models here.

admin.site.register(RSGETaxonomieData)
admin.site.register(RSGEVotingsData)
admin.site.register(otherVotingsData)
admin.site.register(votesData)
admin.site.register(personsData)


