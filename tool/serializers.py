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
        fields = '__all__'
    
