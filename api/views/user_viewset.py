
from api.models import User
from api.serializers import UserSerializer, MyTokenObtainPairSerializer
from api.permissions import IsAdmin

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
import random
import string


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_permissions(self):
        if self.action == 'create' or self.action == 'perform_create':
            permission_classes = [IsHimselfOrSuperUser]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class MyUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset[0])
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):

        queryset = self.list()
        serializer = UserSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def mail_confirm(request):
    if request.method == "POST":
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(6))
        return send_mail(
            'Conformation code',
            f'Your conformation code for authentification is {result_str}.',
            'apostolovdm@gmail.com',
            request.POST['email'],
            fail_silently=False,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        if ("email" in self.request.data) and ("confirmation_code" in self.request.data):
            # if (confirmation_code == confirmation_code):
            return MyTokenObtainPairSerializer
        res = {
            'error': 'can not authenticate with the given credentials or the account has been deactivated'
        }
        return Response(res, status=status.HTTP_403_FORBIDDEN)
