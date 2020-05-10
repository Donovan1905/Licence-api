from django.db import models
from app_companies.models import Company


class Licence(models.Model):
    key = models.CharField(max_length=20)
    company = models.ForeignKey(
        'app_companies.Company',
        on_delete=models.CASCADE
    )
    user_id = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.key
