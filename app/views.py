from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.core.management import call_command

from rest_framework_simplejwt.tokens import RefreshToken

from app.forms import UserForm
from app.serializers import *


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
        if not (user and check_password(password, user.password) and user.deleted_at is None):
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

    def destroy(self, request, pk=None):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')


class InsuranceView(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = InsuranceSerializer
    queryset = Insurance.objects.all()

    def get_queryset(self):
        if 'phone' in self.request.data:
            user = User.objects.filter(phone=self.request.data['phone']).first()
            self.queryset = self.queryset.filter(user=user.id)

        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateView(viewsets.GenericViewSet):

    @action(methods="GET", detail=False)
    def update_status(self, request):
        call_command('seed_commands')
        return Response(
            {
                'message': 'Update successfully'
            },
            status=status.HTTP_200_OK
        )


def upload(request):
    users = User.objects.all()
    context = {"users": users}
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            context["message"] = "Create successfully"
        else:
            context["message"] = "Create failed"
    form = UserForm()
    context["form"] = form
    return render(request, 'upload_image.html', context)
