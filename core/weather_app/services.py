import json
import os
import requests

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
api_key = os.getenv('YANDEX_WEATHER_API_KEY')


class WeatherService:
    @staticmethod
    def get_cached_weather_data(city_name):
        cache_key = f"weather_data_{city_name}"
        return cache.get(cache_key)

    @staticmethod
    def cache_weather_data(city_name, data):
        cache_key = f"weather_data_{city_name}"
        cache.set(cache_key, data, timeout=CACHE_TTL)

    @staticmethod
    def load_city_data():
        with open('weather_app/russian-cities.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def get_weather_data(city_data):
        lat = city_data['coords']['lat']
        lon = city_data['coords']['lon']

        response = requests.get(
            f'https://api.weather.yandex.ru/v1/forecast',
            params={'lat': lat, 'lon': lon},
            headers={'X-Yandex-API-Key': api_key}
        )

        if response.status_code == 200:
            weather_data = response.json()
            return {
                'temperature': weather_data['fact']['temp'],
                'pressure': weather_data['fact']['pressure_mm'],
                'wind_speed': weather_data['fact']['wind_speed']
            }
        else:
            return None
