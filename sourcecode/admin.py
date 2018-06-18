# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import SourceCodeRepo, CodeVersion, CodeVersionGroup
from utils.mixins import AdminCommonUserCanNotDeleteMixin, AdminCanNotDeleteMixin


@admin.register(SourceCodeRepo)
class SourceCodeRepoAdmin(AdminCommonUserCanNotDeleteMixin, admin.ModelAdmin):
    list_display = ('name', 'repo', 'type', 'access_robot')
    radio_fields = {'type': admin.HORIZONTAL}


class CodeVersionGroupInline(admin.StackedInline):
    model = CodeVersionGroup.versions.through
    extra = 0


@admin.register(CodeVersion)
class CodeVersionAdmin(AdminCanNotDeleteMixin, admin.ModelAdmin):
    list_display = ('name', 'repo', 'version', 'release_datetime')


@admin.register(CodeVersionGroup)
class CodeVersionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_versions')
    filter_horizontal = ('versions',)

    def get_versions(self, obj):
        return ["%s:%s" % (v.name, v.version) for v in obj.versions.all()]
    get_versions.short_description = u'版本组合'
