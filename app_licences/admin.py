from django.contrib import admin
from .models import Licence

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'key', 'company')