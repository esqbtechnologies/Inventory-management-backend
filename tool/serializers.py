from rest_framework import serializers
from .models.Usermodels import User


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
