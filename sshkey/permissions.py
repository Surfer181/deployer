# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission


class SSHKeyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        elif request.method.upper() == 'POST':  # 任何人都可以上传key
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        elif user == obj.user:  # 用户可以查看、删除、修改自己的 key
            return True
        else:
            return False


class UserDefaultSSHKeyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.key.user:  # 用户只能修改自己的默认key
            return True
        else:
            return False
