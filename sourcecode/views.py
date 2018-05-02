# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import viewsets, permissions

from . import serializers
from .models import SourceCodeRepo, CodeVersion, CodeVersionGroup
from utils.permissions import IsAdminUserOrReadOnly
from utils.mixins import ActionSerializerMixin


class SourceCodeRepoViewSet(viewsets.ModelViewSet):
    queryset = SourceCodeRepo.objects.all()
    serializer_class = serializers.SourceCodeRepoSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class CodeVersionViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
    queryset = CodeVersion.objects.all()
    serializer_class = serializers.CodeVersionDetailSerializer
    serializer_classes = {
        'list': serializers.CodeVersionListSerializer,
    }
    permission_classes = (IsAdminUserOrReadOnly,)


class CodeVersionGroupViewSet(viewsets.ModelViewSet):
    queryset = CodeVersionGroup.objects.all()
    serializer_class = serializers.CodeVersionGroupSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
