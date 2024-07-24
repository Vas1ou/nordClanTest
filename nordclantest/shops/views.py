from .serializers import ShopSerializer
from .models import Shop
from addresses.models import City, Street
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import get_open_shops, get_closed_shops

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def create(self, request, *args, **kwargs):
        # создаю экземпляр сериализатора
        serializer = self.get_serializer(data=request.data)
        # проверяю валидность данных
        serializer.is_valid(raise_exception=True)
        # создаю новый экземпляр модели
        self.perform_create(serializer)
        # формирую заголовок, в случае успешного сохранения в базу
        headers = self.get_success_headers(serializer.data)
        # тут меняю статус на 200 (так в условии) знаю, что тут должен быть другой, но решил поменять
        return Response({'id': serializer.data['id']}, status=status.HTTP_200_OK, headers=headers)

    def list(self, request, *args, **kwargs):
        # Получаю начальный queryset (тут нагуглил, что хорошей практикой будет получать через filter_queryset)
        queryset = self.filter_queryset(self.get_queryset())

        # Получаю параметры GET запроса
        street_id = request.query_params.get('street')
        city_id = request.query_params.get('city')
        open_status = request.query_params.get('open')

        # Переменная, в которой хранится время в текущем городе
        time_in_town = None

        if city_id:
            try:
                city = City.objects.get(pk=city_id)
                # Получаю текущее время в городе
                time_in_town = city.current_time
                if street_id:
                    # Проверю, что бы улица принадлежала городу
                    if Street.objects.filter(pk=street_id, city_id=city_id).exists():
                        queryset = queryset.filter(city_id=city_id, street_id=street_id)
                    else:
                        return Response({'error': f'Улица с id {street_id} не принадлежит городу с id {city_id}'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    queryset = queryset.filter(city_id=city_id)

            except City.DoesNotExist:
                return Response({'error': f'Город с id - {city_id} отсутствует в базе данных'},
                                status=status.HTTP_400_BAD_REQUEST)

        elif street_id:
            try:
                street = Street.objects.get(pk=street_id)
                # Получаю текущее время в городе
                time_in_town = street.city.current_time
                queryset = queryset.filter(street_id=street_id)
            except Street.DoesNotExist:
                return Response({'error': f'Улица с id - {street_id} отсутствует в базе данных'})

        """
        Я отфильтровал данные по городу и улице (если они были), так же проверил, что бы объект street 
        принадлежал city.
        Далее, необходимо определить, в итоговом queryset открыты ли магазины или нет
        (скорей всего, надо было это делать в одном запросе, понимаю... )
        """
        if open_status == '1':
            # Необходимо вернуть все магазины с текущего города, которые открыты
            if time_in_town:
                queryset = queryset.filter(opening_time__lte=time_in_town, closing_time__gte=time_in_town)

            # Необходимо вернуть все открытые магазины на текущий момент
            else:
                queryset = get_open_shops(queryset)
        elif open_status == '0':
            # Необходимо отдать все магазины с текущего города, которые закрыты
            if time_in_town:
                queryset = queryset.exclude(opening_time__lte=time_in_town, closing_time__gte=time_in_town)

            # Необходимо вернуть все закрытые магазины на текущий момент
            else:
                queryset = get_closed_shops(queryset)

        # Сериализация и возврат данных
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
