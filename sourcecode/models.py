# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid

from django.db import models

from account.models import Robot
from utils.constants import MAX_LENGTH


class SourceCodeRepo(models.Model):
    TYPE_CHOICES = (
        ("git", "git"),
        ("svn", "svn"),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=MAX_LENGTH['name'], verbose_name=u'名称')
    repo = models.CharField(max_length=MAX_LENGTH['url'], verbose_name=u'代码仓库地址')
    type = models.CharField(choices=TYPE_CHOICES, max_length=MAX_LENGTH['type_choices'],
                            default='git', verbose_name=u'SVN/Git')
    access_robot = models.ForeignKey(Robot, verbose_name=u'使用哪个用户')

    class Meta:
        verbose_name = u"代码仓库"
        verbose_name_plural = u"代码仓库"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.repo)


class CodeVersion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=MAX_LENGTH['name'], verbose_name=u'名称')
    version = models.CharField(max_length=MAX_LENGTH['code_version'], verbose_name=u'版本号')
    repo = models.ForeignKey(SourceCodeRepo)
    release_datetime = models.DateTimeField(blank=True, null=True, verbose_name=u'发布时间')
    release_note = models.TextField(blank=True, null=True, verbose_name=u'Release Note')

    class Meta:
        verbose_name = u"代码版本号"
        verbose_name_plural = u"代码版本号"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.version)


class CodeVersionGroup(models.Model):
    # TODO: 改名为 CodeRelease
    """
    记录版本号对应关系
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=MAX_LENGTH['name'], verbose_name=u'名称')
    versions = models.ManyToManyField(CodeVersion, verbose_name=u'版本组合',
                                      help_text=u'eg: 后端v1.0,前端v1.0.1,移动端v0.5')
    desc = models.TextField(blank=True, null=True, verbose_name=u'描述')

    class Meta:
        verbose_name = u"代码包"
        verbose_name_plural = u"代码包"

    def __unicode__(self):
        return self.name
