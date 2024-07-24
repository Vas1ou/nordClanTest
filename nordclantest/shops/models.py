from django.db import models
from addresses.models import City, Street


class Shop(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='shops', on_delete=models.CASCADE)
    street = models.ForeignKey(Street, related_name='shops', on_delete=models.CASCADE)
    house_number = models.CharField(max_length=10)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"'{self.name}' г. {self.city.name}, ул. {self.street.name}, д. {self.house_number}"
