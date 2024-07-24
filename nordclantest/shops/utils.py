def get_open_shops(qs):
    open_shops = []

    for shop in qs:
        # Получаю время в городе, в котором находится магазин
        city_time = shop.city.current_time

        # Получаю время открытия и закрытия магазина
        opening_time = str(shop.opening_time)
        closing_time = str(shop.closing_time)

        # Проверяю, открыт ли магазин
        if opening_time <= city_time <= closing_time:
            open_shops.append(shop)

    return open_shops


def get_closed_shops(qs):
    closed_shops = []

    for shop in qs:
        # Получаю время в городе, в котором находится магазин
        city_time = shop.city.current_time

        # Получаю время открытия и закрытия магазина
        opening_time = str(shop.opening_time)
        closing_time = str(shop.closing_time)

        # Проверяю, открыт ли магазин
        if not (opening_time <= city_time <= closing_time):
            closed_shops.append(shop)

    return closed_shops
