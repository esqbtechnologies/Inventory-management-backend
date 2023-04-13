from django.db import models
from .Locationmodels import location
# from .Verificationmodels import verification
# from .Qrmodels import Qr


class asset(models.Model):
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=200)
    asset_cls = models.CharField(max_length=200,blank = True,null = True)
    periodcat = models.CharField(max_length=200,blank = True,null = True)
    Useful_life = models.CharField(max_length=200,blank = True,null = True)
    Remain_life = models.CharField(max_length=200,blank = True,null = True)
    Warehouse_location = models.ForeignKey(location,blank = True,null = True,on_delete=models.SET_NULL)
    Qr_id = models.CharField(max_length=500, null=True, blank=True)
    is_deleted = models.BooleanField(default = False)
    amount = models.IntegerField(blank = True, null = True)
    def __str__(self):
        return self.item_code
    # verification_id = models.ForeignKey(
    #     verification, on_delete=models.SET_NULL, null=True)
