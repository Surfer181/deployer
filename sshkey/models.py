# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

from django.db import models
from django.conf import settings as django_settings

from .utils import pubkey_parse
from .exceptions import PublicKeyTypeError
from utils.mixins import CreateLastUpdateDatetimeAbstractModel


class UserKey(CreateLastUpdateDatetimeAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    key = models.TextField(max_length=2000)
    fingerprint = models.CharField(max_length=128, blank=True, db_index=True)

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.name)

    class Meta:
        unique_together = ('user', 'name')

    def clean(self):
        self.key = self.key.strip()
        if not self.key:
            return
        pubkey = pubkey_parse(self.key)
        self.key = pubkey.format_openssh()
        self.fingerprint = pubkey.fingerprint()
        if not self.name:
            if pubkey.comment:
                self.name = pubkey.comment

    def export(self, format='RFC4716'):
        pubkey = pubkey_parse(self.key)
        f = format.upper()
        if f == 'RFC4716':
            return pubkey.format_rfc4716()
        if f == 'PEM':
            return pubkey.format_pem()
        raise PublicKeyTypeError

    def save(self, *args, **kwargs):
        self.clean()
        return super(UserKey, self).save(*args, **kwargs)


class UserDefaultSSHkey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL)
    key = models.ForeignKey(UserKey)

    class Meta:
        unique_together = ('user', 'key')  # 每人一个默认key

    def __unicode__(self):
        return self.user.full_name if self.user.full_name else self.user.username
