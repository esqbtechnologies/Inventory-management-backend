from rest_framework import serializers
from .models.Usermodels import User
from .models.Assetmodels import asset

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class Assetserializer(serializers.ModelSerializer):
    class Meta:
        model = asset
        fields = [ 'item_code',
                 'item_name',
                 'asset_cls',
                 'periodcat',
                 'Useful_life',
                 'Remain_life',
                 'Warehouse_location',
                 'Qr_id',]
              
