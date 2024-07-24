from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404


#  Создаю обработчик, что бы при любой ошибке возвращался статус 400
class CustomErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Проверка исключений, которые могут быть проигнорированы
        if isinstance(exception, Http404):
            print(exception)
            return JsonResponse({'detail': 'Not Found'}, status=404)
        return JsonResponse({'detail': str(exception)}, status=400)
