from rest_framework import serializers


class WeatherDataSerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    pressure = serializers.IntegerField()
    wind_speed = serializers.FloatField()
