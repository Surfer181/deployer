# -*- coding: utf-8 -*-

"""
为 django 补充了几个常用的 validator
"""

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


def validate_has_key(data, key):
    if key not in data:
        raise serializers.ValidationError({
            key: _('this field is required')
        })


PHONE_RE = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=_("phone number should be: 9-15 pure number")
)

POST_CODE_RE = RegexValidator(
    regex=r'^\d{6}$',
    message=_("post code should be 6 pure number")
)

POINT_RE = RegexValidator(
    regex=r'^\((-|\+)?\d{1,6},\s*(-|\+)?\d{1,6}\)$',
    message=_("point should be format of (12345, 12345)")
)

HEX_RE = RegexValidator(
    regex=r'^#{0,1}[A-Fa-f0-9]+$',
    message=_("hex should be format of #{0,1}[A-Fa-f0-9]+")
)
