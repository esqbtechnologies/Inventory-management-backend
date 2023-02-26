from enum import unique
from django.db import models

from .Usermodels import User
from .Assetmodels import asset


class verification(models.Model):
    geo_location = models.CharField(max_length=500)
    date = models.DateField()
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    asset = models.ForeignKey(
        asset, on_delete=models.CASCADE, unique=False, null=True)
    sessionId = models.CharField(max_length=200)

    def int(self):
        return self.pk
