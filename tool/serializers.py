from rest_framework import serializers
from .models.Usermodels import User
from .models.Assetmodels import asset
from .models.Locationmodels import location

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class locationserializer(serializers.ModelSerializer):
    class meta:
        model = location
        fields = '__all__'

class Assetserializer(serializers.ModelSerializer):
    Warehouse_location = locationserializer(read_only = True)    
    class Meta:
        model = asset
        fields = '__all__'
              
              
