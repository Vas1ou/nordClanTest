from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # Отображаю все поля модели в админке
    list_display = [field.name for field in Shop._meta.fields]
    search_fields = ('name', 'city__name', 'street__name', 'opening_time', 'closing_time')
    list_filter = ('city', 'street')
