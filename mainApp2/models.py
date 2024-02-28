from django.db import models

class WeatherForecast(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=100)
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    total_precipitation = models.FloatField()
    weather_description = models.CharField(max_length=255)
    pressure = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.city}"
