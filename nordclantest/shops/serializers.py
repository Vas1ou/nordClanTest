from rest_framework import serializers
from .models import Shop
from addresses.models import City, Street
from django.core.exceptions import ObjectDoesNotExist


class ShopSerializer(serializers.ModelSerializer):
    # Поля для ввода идентификаторов города и улицы
    city_id = serializers.IntegerField(write_only=True)
    street_id = serializers.IntegerField(write_only=True)

    # Поля для отображения имен города и улицы
    city = serializers.CharField(source='city.name', read_only=True)
    street = serializers.CharField(source='street.name', read_only=True)

    class Meta:
        model = Shop
        # Понимаю, что all может влиять на производительность, но мне нужны все поля, в любом случае
        fields = "__all__"

    # Решил добавить кое-какую доп.валидацию + решил сделать невозможным добавление магазина, если улица не
    # содержится в городе.
    def create(self, validated_data):
        # Извлечение данных для связанных объектов
        city_id = validated_data.pop('city_id', None)
        street_id = validated_data.pop('street_id', None)

        # Попытка получения города по идентификатору
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            raise serializers.ValidationError({'error': f'Город с id - {city_id} отсутствует в базе данных'})

        # Попытка получения улицы по идентификатору
        try:
            street = Street.objects.get(id=street_id)
        except Street.DoesNotExist:
            raise serializers.ValidationError({'error': f'Улица с id - {street_id} отсутствует в базе данных'})

        # Решил еще перед сохранением объекта, проверять, что улица принадлежит этому городу
        if street.city != city:
            raise serializers.ValidationError({
                'error': f'{street} не принадлежит городу {city}'
            })

        # Создание нового магазина
        shop = Shop.objects.create(
            city=city,
            street=street,
            **validated_data
        )
        return shop
