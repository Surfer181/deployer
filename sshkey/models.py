# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

from django.db import models
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .utils import PublicKeyParseError, pubkey_parse
from utils.mixins import CreateLastUpdateDatetimeMixin


class UserKey(CreateLastUpdateDatetimeMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    key = models.TextField(max_length=2000)
    fingerprint = models.CharField(max_length=128, blank=True, db_index=True)

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.name)

    def clean_fields(self, exclude=None):
        if not exclude or 'key' not in exclude:
            self.key = self.key.strip()
            if not self.key:
                raise ValidationError({'key': [_("This field is required.")]})

    def clean(self):
        self.key = self.key.strip()
        if not self.key:
            return
        try:
            pubkey = pubkey_parse(self.key)
        except PublicKeyParseError as e:
            raise ValidationError(str(e))
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
        raise ValueError(_("Invalid format"))
