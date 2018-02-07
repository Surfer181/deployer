# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserKey, UserDefaultSSHkey
from . import serializers, permissions
from utils.mixins import ActionSerializerMixin


class UserKeyViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
    queryset = UserKey.objects.all()
    serializer_class = serializers.UserKeyDetailSerializer
    serializer_classes = {
        'list': serializers.UserKeyListSerializer,
    }
    permission_classes = (IsAuthenticated, permissions.SSHKeyPermission)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super(UserKeyViewSet, self).create(request, *args, **kwargs)


class UserDefaultSSHkeyViewSet(viewsets.ModelViewSet):
    queryset = UserDefaultSSHkey.objects.all()
    serializer_class = serializers.UserDefaultSSHkeySerializer
    permission_classes = (IsAuthenticated, permissions.UserDefaultSSHKeyPermission)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super(UserDefaultSSHkeyViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return UserDefaultSSHkey.objects.filter(user=self.request.user)
