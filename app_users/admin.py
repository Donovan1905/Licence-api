from django.contrib import admin
from .models import FakeUser

@admin.register(FakeUser)
class FakeUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'company')