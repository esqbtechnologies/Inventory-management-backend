from django.db import models
from .Locationmodels import location

class session(models.Model):
    sessionId = models.CharField(max_length=200)
    sessionStartDate = models.DateField()
    sessionEndDate = models.DateField(null=True)
    isActive = models.BooleanField()
    location = models.ForeignKey(location,blank = True,null = True,on_delete= models.SET_NULL)
    is_latest = models.BooleanField(default = True)
