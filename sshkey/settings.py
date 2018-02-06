# -*- coding: utf-8 -*-
from django.conf import settings

SSHKEY_AUTHORIZED_KEYS_OPTIONS = getattr(settings, 'SSHKEY_AUTHORIZED_KEYS_OPTIONS', None)
SSHKEY_ALLOW_EDIT = getattr(settings, 'SSHKEY_ALLOW_EDIT', False)
SSHKEY_DEFAULT_HASH = getattr(settings, 'SSHKEY_DEFAULT_HASH', 'legacy')
