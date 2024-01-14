from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import WeatherService
from weather_app.serializers import WeatherDataSerializer


class WeatherAPIView(APIView):
    def get(self, request, *args, **kwargs):
        city_name = request.query_params.get('city')
        if not city_name:
            return Response({'error': 'No city provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, есть ли уже кэшированные данные
        cached_data = WeatherService.get_cached_weather_data(city_name)
        if cached_data:
            # Если данные в кэше, возвращаем их
            return Response(cached_data)

        # Загрузка данных о городах
        cities = WeatherService.load_city_data()

        # Поиск координат города
        city_data = next((city for city in cities if city["name"].lower() == city_name.lower()), None)
        if not city_data:
            return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

        weather_data = WeatherService.get_weather_data(city_data)

        if weather_data is not None:
            WeatherService.cache_weather_data(city_name, weather_data)
            serializer = WeatherDataSerializer(data=weather_data)
            if serializer.is_valid():
                return Response(serializer.validated_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Failed to get weather data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
