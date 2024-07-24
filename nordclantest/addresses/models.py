from django.db import models
from pytz import all_timezones, timezone
from datetime import datetime


class City(models.Model):
    name = models.CharField(max_length=100)
    # При добавлении города необходимо будет указать timezone
    timezone = models.CharField(max_length=100, choices=[(tz, tz) for tz in all_timezones])

    def __str__(self):
        return f'г. {self.name}'

    @property
    def current_time(self):
        """Получаю время в городе, учитывая часовой пояс"""
        city_timezone = timezone(self.timezone)
        city_time = datetime.now(city_timezone).strftime('%H:%M:%S')

        return city_time


class Street(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='streets', on_delete=models.CASCADE)

    def __str__(self):
        return f'г. {self.city.name} ул. {self.name}'
