from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Получение токена из заголовка
        token = request.headers.get('Authorization')
        if not token:
            Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if token == 'NordClanSecretTokenValue':
            return (None, None)
        else:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

