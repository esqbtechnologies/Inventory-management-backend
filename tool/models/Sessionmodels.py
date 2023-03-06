from django.db import models


class session(models.Model):
    sessionId = models.CharField(max_length=200)
    sessionStartDate = models.DateField()
    sessionEndDate = models.DateTimeField(null=True)
    isActive = models.BooleanField()
