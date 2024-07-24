from .serializers import CitySerializer, StreetSerializer
from .models import City, Street
from rest_framework import viewsets


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StreetSerializer

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')
        if city_id:
            return Street.objects.filter(city_id=city_id)
        return Street.objects.all()
