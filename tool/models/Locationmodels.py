from django.db import models


class location(models.Model):
    lname = models.CharField(max_length=300,unique= True)

    def __str__(self):
        return self.lname