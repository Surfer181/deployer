# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from .models import UserKey, UserDefaultSSHkey
from account.serializers import UserIdNameSerializer
from utils.mixins import ResponseDetailMixin


class UserKeyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = '__all__'


class UserKeyListSerializer(ResponseDetailMixin, serializers.ModelSerializer):
    class Meta:
        model = UserKey
        exclude = ('fingerprint', 'key')
        detail_serializers = {
            'user': UserIdNameSerializer
        }


class UserDefaultSSHkeySerializer(ResponseDetailMixin, serializers.ModelSerializer):
    class Meta:
        model = UserDefaultSSHkey
        fields = '__all__'
        detail_serializers = {
            'user': UserIdNameSerializer
        }
