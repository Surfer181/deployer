# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    """
    登录用户，如果是管理员，则可编辑，否则只读
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated() and (
                request.method in SAFE_METHODS or
                request.user.is_staff
            )
        )


class IsAdminUserOrCreateOnly(BasePermission):
    """
    登录用户，如果是管理员，则可编辑，否则只能创建
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated() and (
                request.method in SAFE_METHODS or
                request.method == 'POST' or
                request.user.is_staff
            )
        )


class IsSafeMethodOrAdminUser(BasePermission):
    """
    是SafeMethod 和管理员才允许
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user and request.user.is_staff
            )
        )
