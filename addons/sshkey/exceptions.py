# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.utils.translation import ugettext as _

from utils.exceptions import GenericException


class PublicKeyParseError(GenericException):
    status_code = 400
    default_detail = _("Unrecognized public key format")
    error_code = 11001


class PublicKeyTypeError(GenericException):
    status_code = 400
    default_detail = _("Invalid format")
    error_code = 11002
