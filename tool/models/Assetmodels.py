from django.db import models

# from .Verificationmodels import verification
# from .Qrmodels import Qr


class asset(models.Model):
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=200)
    asset_cls = models.CharField(max_length=200)
    periodcat = models.CharField(max_length=200)
    Useful_life = models.CharField(max_length=200)
    Remain_life = models.CharField(max_length=200)
    Warehouse_location = models.CharField(max_length=200)
    Qr_id = models.CharField(max_length=500, null=True, blank=True)
    is_deleted = models.BooleanField(default = False)
    
    def __str__(self):
        return self.item_code
    # verification_id = models.ForeignKey(
    #     verification, on_delete=models.SET_NULL, null=True)
