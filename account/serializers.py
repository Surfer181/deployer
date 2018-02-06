# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'is_active',
                  'date_joined', 'full_name', 'phone1', 'phone2', 'avatar')


class UserIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'username')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = u"当前用户处于未激活状态"
                    raise exceptions.ValidationError(msg)
            else:
                msg = u"登录验证失败"
                raise exceptions.ValidationError(msg)

        else:
            msg = u"请输入用户名和密码"
            raise exceptions.ValidationError(msg)

        token, created = Token.objects.get_or_create(user=user)

        attrs['user'] = user
        attrs['token'] = token.key
        return attrs
