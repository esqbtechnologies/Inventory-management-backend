from django.db import models
from .Usermodels import User


class otp(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    num = models.IntegerField()
    date = models.DateTimeField()
    flag = models.BooleanField(default=False)
