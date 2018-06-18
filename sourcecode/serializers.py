# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from .models import SourceCodeRepo, CodeVersion, CodeVersionGroup
from account.serializers import RobotIdNameSerializer
from utils.mixins import ResponseDetailMixin


class SourceCodeRepoSerializer(ResponseDetailMixin, serializers.ModelSerializer):

    class Meta:
        model = SourceCodeRepo
        fields = "__all__"
        detail_serializers = {
            'access_robot': RobotIdNameSerializer
        }


class SourceCodeRepoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceCodeRepo
        fields = ['uuid', 'name', 'repo']


class CodeVersionListSerializer(ResponseDetailMixin, serializers.ModelSerializer):

    class Meta:
        model = CodeVersion
        exclude = ['release_note']
        detail_serializers = {
            'repo': SourceCodeRepoSimpleSerializer
        }


class CodeVersionDetailSerializer(ResponseDetailMixin, serializers.ModelSerializer):

    class Meta:
        model = CodeVersion
        fields = '__all__'
        detail_serializers = {
            'repo': SourceCodeRepoSimpleSerializer
        }


class CodeVersionGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeVersionGroup
        fields = '__all__'
