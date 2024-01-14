from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache


class WeatherAPITestCase(APITestCase):
    mock_city_data = [
        {
            "coords": {
                "lat": "54.71667",
                "lon": "20.5"
            },
            "district": "Северо-Западный",
            "name": "Калининград",
            "population": 490449,
            "subject": "Калининградская область"
        }
    ]

    def setUp(self):
        self.api_url = reverse('weather_api')
        self.city_name_valid = "Калининград"
        self.city_name_invalid = "Неверный-город"
        self.mock_weather_data = {
            'fact': {
                'temp': -1,
                'feels_like': -6,
                'pressure_mm': 751,
                'pressure_pa': 1001,
                'wind_speed': 4
            }
        }

    def tearDown(self):
        cache.clear()

    @patch('requests.get')
    @patch('weather_app.services.WeatherService.load_city_data')
    def test_weather_api_valid_city(self, mock_load_city, mock_get):
        mock_load_city.return_value = self.mock_city_data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_weather_data

        response = self.client.get(self.api_url, {'city': self.city_name_valid})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature'], self.mock_weather_data['fact']['temp'])

    def test_weather_api_city_not_found(self):
        response = self.client.get(self.api_url, {'city': self.city_name_invalid})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_weather_api_no_city(self):
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_weather_api_caching(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_weather_data

        # Первый запрос должен сохранить данные в кэш
        self.client.get(self.api_url, {'city': self.city_name_valid})
        self.assertIn(f'weather_data_{self.city_name_valid}', cache)

        # Второй запрос должен использовать данные из кэша
        response = self.client.get(self.api_url, {'city': self.city_name_valid})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get.assert_called_once()  # Убеждаемся, что внешний API вызван только один раз
