from enum import unique
from django.db import models

from .Usermodels import User
from .Assetmodels import asset


class verification(models.Model):
    geo_location = models.CharField(max_length=500)
    date_time = models.DateTimeField()
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    asset = models.ForeignKey(
        asset, on_delete=models.CASCADE, unique=False, null=True)

    def int(self):
        return self.pk
