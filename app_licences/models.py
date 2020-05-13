from django.db import models
from app_companies.models import Company
from app_users.models import CustomUser


class Licence(models.Model):
    key = models.CharField(max_length=20, unique=True)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        'app_users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.key
