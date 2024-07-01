import requests
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

class HelloView(View):
    @method_decorator(csrf_exempt)
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = request.META.get('REMOTE_ADDR')
        
        # Get location data from IP address
        location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
        location_data = location_response.json()
        city = location_data.get('city', 'Unknown')
        
        # Fetch temperature for the city
        weather_api_key = os.getenv('WEATHER_API_KEY')
        weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}')
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        
        response_data = {
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {visitor_name.strip('"')}!, the temperature is {temperature} degrees Celsius in {city}"
        }
        return JsonResponse(response_data)
