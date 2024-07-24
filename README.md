## nordClanTest - Тестовое задание 
### Задание:
#### shop Реализовать сервис, который принимает и отвечает на HTTP запросы.
- #### В случае успешной обработки сервис должен
  - отвечать статусом 200, в случае любой ошибки — статус 400.
- #### Запросы (GET)
  - `/citi/` - получение всех городов из базы;
  - `city//street` - получение всех улиц города;
  - `/shop/?street=&city=&open=0/1` - получение списка магазинов
      - ##### Метод принимает параметры для фильтрации.
              Параметры не обязательны. В случае отсутствия
              параметров выводятся все магазины, если хоть
              один параметр есть , то по нему выполняется
              фильтрация.
      - ##### Важно!
              в объекте каждого магазина
              выводится название города и улицы, а не id
              записей.
      - ##### Параметр open
              0 - закрыт, 1 - открыт. Данный
              статус определяется исходя из параметров
              «Время открытия», «Время закрытия» и текущего
              времени сервера.
- #### Запросы (POST)
  - `/shop/` - создание магазина. Данный метод получает json c объектом магазина, в ответ возвращает id созданной записи.
- #### Объекты:
    - ##### Магазин
          Название
          Город
          Улица
          Дом
          Время открытия
          Время закрытия
  - ##### Город
          Название 
  - ##### Улица
          Название
          Город
- #### Важно: Выстроить связи между таблицами в базе данных.
- #### Инструменты:
    - Любой веб-фреймворк на Python
    - Реляционная БД (PostgreSQL - предпочтительно, MySQL и тд) p.s. Использовал Postgres
    - Запросы в базу данных через ORM (ORM на выбор). p.s. использовал Django ORM

### Выполнение:
  #### Для начала определил объем работы (задача показалась не особо сложной, по крайней мере, я уже предполагал, как я это сделаю). Объем чуть превзошел мои ожидания :)
  - Создал проект, в нем решил создать Два приложения отдельное для магазинов и отдельное для адресов т.к. так будет удобнее использовать адреса и с другими объектами.
    ```
    nordclantest/
    │
    ├── adresses/
    │   ├── __init__.py
    │   ├── models.py
    │   └── views.py
    │
    ├── shops/
    │   ├── __init__.py
    │   ├── models.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    ```
  - Затем решил реализовать, что бы при любой ошибке сервер возвращал status 400
    ```python
    #  Создаю обработчик, что бы при любой ошибке возвращался статус 400
    class CustomErrorMiddleware(MiddlewareMixin):
        def process_exception(self, request, exception):
            # Проверка исключений, которые могут быть проигнорированы
            if isinstance(exception, Http404):
                print(exception)
                return JsonResponse({'detail': 'Not Found'}, status=404)
            return JsonResponse({'detail': str(exception)}, status=400)
    ```
    тут я исключил 404, решил сделать так
- Далее создал модели магазина, города и улицы.
- Затем написал сериализаторы для всех моделей.


  Сериализаторы самые простые, за исключением сериализатора для магазинов (в задании указано, что получать я должен не id улицы и города, а их названия)
  ```python
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
  ```
  тут решил добавить доп. валидацию + проверять, что бы улица магазина - принадлежала его городу. p.s. в случае любой ошибки я получаю статус 400, как говорилось выше.

  - Далее першел к вьюхам и адресам, код, думаю, удобнее будет смотреть в проекте.
  #### То есть на данном этапе я реализовал все GET запросы + POST запрос с добавлением магазина, оставалось сделать только получение списка магазинов по параметрам.
  #### Получить города по фильтрам (улица, город) не сложно, начал думать как мне учитывать время при получении закрытых (open=0) и открытых (open=1) магазинов.
  #### P.S. вопросов не задавал специально, решил выполнить задание максимально объемно, как я это понимаю, так сказать "под ключ" (надеюсь получилось)
    - ##### Я понимал, что мне в любом случае, в момент запроса (речь сейчас идет только про параметр open) необходимо определять местное время в городе, в котором находится магазин.
      ##### Вариантов было несколько:
        - Получать время в городе из стороннего сервиса. Вот сервис с которым я уже работал, он бесплатный, можно получить время в любом городе [DaData](https://dadata.ru/api/clean/)
        - Хранить разницу во времени между городом и текущим временем сервера
        - Хранить часовой пояс города, в которм находятся магазины.

    Скорей всего, думаю, ожидалось, как я понял по заданию, что я буду хранить разницу во времени между городом и текущим временем сервера.
    Использовать сторонний сервис не стал (думаю, что надежнее будет, если данные о времени хранятся у меня)
    В итоге я решил хранить часовой пояс города, именно часовой пояс, а не разницу межд временем города и временем сервера.
    Постараюсь аргументировать. Вне зависимости от времени сервера, я буду получать точное время в городе. Тут есть минус, который меня беспокоит и из за которого я переживаю это то, что в задании в моделе
    City было только поле name (опять же разницу во времени тоже надо было где-то ххранить) + не знаю, такой ли реализации от меня ожидали.

  #### Итог:
  - Добавил поле timezone в модель City
    ```python
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
    ```
    Так же написал метод для получения текущего времени в городе.


##### В ShopViewSet переопределил метод list для получения объектов модели магазинов. Так же добавил доп. валидацию (если улица не принадлежит городу) p.s. В случае возникновения любой ошибки - вернется статус 400

  ```python
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
  ```

#### Для удобного добавления Улиц и Городов, добавил все модели в Админку (login - admin, password - 1234)
![image](https://github.com/user-attachments/assets/ff488a5c-095d-4603-a1dc-5006ee9d29f7)
![image](https://github.com/user-attachments/assets/0433c953-7c5b-470c-96f4-8579798b1c18)

#### Ну и напоследок скажу, что запросы потестил, все работает, ниже приложу скрины с запросами (Очень жду обратной связи по тестовому заданию)
![image](https://github.com/user-attachments/assets/46114dc9-c76c-4a58-b229-ae07b221bd23)
![image](https://github.com/user-attachments/assets/2bacea1a-d7eb-43a5-97fb-1584d2e0deb0)
![image](https://github.com/user-attachments/assets/3f9227a7-8838-4be3-9c6c-f45c54dca379)
![image](https://github.com/user-attachments/assets/0e60e961-2fa6-43ca-b622-376ec4f18446)







