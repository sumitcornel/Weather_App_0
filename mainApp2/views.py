import urllib.request
import json
from django.shortcuts import render
from datetime import datetime
from .models import WeatherForecast

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')

        
        forecast_list = []

        try:
            
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q=' +
                                            city + '&units=metric&appid=d2f2daf1b8e885670d78407207c04fbd').read()
            forecast_data = json.loads(source)['list']

            
            for forecast in forecast_data:
                date = (datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')).date()
                if date not in [item['date'] for item in forecast_list]:
                    max_temp = -273.15  
                    min_temp = 1000     
                    precipitation = 0
                    weather_description = ''
                    pressure = 0
                    humidity = 0
                    wind_speed = 0
                    for item in forecast_data:
                        if (datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')).date() == date:
                            max_temp = max(max_temp, item['main']['temp_max'])
                            min_temp = min(min_temp, item['main']['temp_min'])
                            precipitation += item['rain']['3h'] if 'rain' in item else 0
                            weather_description = item['weather'][0]['description']
                            pressure = item['main']['pressure']
                            humidity = item['main']['humidity']
                            wind_speed = item['wind']['speed']
                    forecast_list.append({
                        'date': date,
                        'max_temp': round(max_temp, 2),
                        'min_temp': round(min_temp, 2),
                        'precipitation': round(precipitation, 2),
                        'weather_description': weather_description,
                        'pressure': pressure,
                        'humidity': humidity,
                        'wind_speed': wind_speed
                    })

        except Exception as e:
            
            error_message = f"Error fetching weather forecast data: {str(e)}"
            return render(request, "main/error.html", {'error_message': error_message})

        
        data = {'forecast_list': forecast_list}
        return render(request, "main/index.html", data)

    else:
        return render(request, "main/index.html")
