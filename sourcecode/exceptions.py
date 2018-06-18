# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from utils.exceptions import GenericException


class NotGitRepoError(GenericException):
    status_code = 400
    default_detail = _('This is not a Git repo!')
    error_code = 20001
