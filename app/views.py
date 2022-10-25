from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password

from rest_framework import status, serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken

from app.models import User
from app.serializers import LoginUserSerializer, UserSerializer


@permission_classes([AllowAny])
class LoginUserApi(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=user)[0].key
        if not (user and check_password(password, user.password) and not user.is_deleted):
            raise serializers.ValidationError({'detail': 'Incorrect username, password or account has been deleted'})

        login(request, user)
        # Generate Token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'expires_in': datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                },
                'auth': {
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'address': user.address,
                }
            },
            status=status.HTTP_200_OK
        )


class Logout(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, pk=None):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')
