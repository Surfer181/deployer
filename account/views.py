# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import parsers, viewsets, status, generics, mixins
from rest_framework.filters import SearchFilter

from . import serializers
from .models import User


class LoginView(generics.GenericAPIView):
    """
    登录
    HTTP Method: POST
    """
    permission_classes = (AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        kwargs = dict()
        kwargs['context'] = self.get_serializer_context()
        serializer = serializers.UserDetailSerializer(user, **kwargs)

        ret = {
            'token': token,
            'user': serializer.data,
        }
        return Response(ret, status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ("full_name", "phone1", "phone2")
