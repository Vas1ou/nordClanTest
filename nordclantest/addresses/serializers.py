from rest_framework import serializers
from .models import City, Street


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ['id', 'name', 'city']
