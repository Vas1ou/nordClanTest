from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, StreetViewSet

# Создаю экземпляр DefaultRouter
router = DefaultRouter()

router.register(r'', CityViewSet, basename='city')
router.register(r'(?P<city_id>\d+)/street', StreetViewSet, basename='street')

urlpatterns = [
    path('', include(router.urls)),
]
