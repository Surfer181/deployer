# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from utils.constants import MAX_LENGTH
from utils import validators
from utils.commands import ssh_rsa_key_gen, check_make_local_dir


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=MAX_LENGTH['name'], null=True, blank=True, verbose_name=u'姓名')
    phone1 = models.CharField(validators=[validators.PHONE_RE], max_length=MAX_LENGTH['phone'],
                              blank=True, verbose_name=u'手机号1')
    phone2 = models.CharField(validators=[validators.PHONE_RE], max_length=MAX_LENGTH['phone'],
                              blank=True, verbose_name=u'手机号2')
    avatar = models.ImageField(upload_to='users/avatar/', blank=True, null=True, verbose_name=u'头像')

    def __unicode__(self):
        return "%s(%s)" % (self.username, self.id)


class Robot(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=MAX_LENGTH['name'], verbose_name=u'名称')
    private_key_path = models.FilePathField(path='.', editable=False)
    public_key_path = models.FilePathField(path='.', editable=False)
    detail = models.TextField(blank=True, null=True, verbose_name=u'描述')

    class Meta:
        verbose_name = u"机器人"
        verbose_name_plural = u"机器人"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.private_key_path or not self.public_key_path:
            # TODO: 数据库里面存的是绝对路径,如果更改了项目启动的目录就需要修数据
            key_dir_name = os.path.join(settings.SSHKEY_DIR, str(self.uuid))
            check_make_local_dir(key_dir_name)
            key_name = os.path.join(key_dir_name, "id_rsa")
            self.private_key_path, self.public_key_path = ssh_rsa_key_gen(key_name, user=str(self.uuid))
        return super(Robot, self).save(*args, **kwargs)
