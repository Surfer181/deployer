# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.constants import MAX_LENGTH
from utils import validators


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
