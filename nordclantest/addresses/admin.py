from django.contrib import admin
from .models import City, Street


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)



