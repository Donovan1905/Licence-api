from __future__ import unicode_literals
from django.db import models
from app_companies.models import Company
from django.utils.translation import ugettext_lazy as _


class FakeUser(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )