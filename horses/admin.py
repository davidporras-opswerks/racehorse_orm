from django.contrib import admin
from .models import Jockey, Racehorse, Race, Participation

admin.site.register(Jockey)
admin.site.register(Racehorse)
admin.site.register(Race)
admin.site.register(Participation)

# Register your models here.
