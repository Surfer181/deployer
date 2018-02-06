from django.utils.translation import ugettext as _
from rest_framework.exceptions import APIException


class GenericException(APIException):
    status_code = 400
    default_detail = _('Unknown error.')
    error_code = 10000
    dict_detail = None

    def __init__(self, message=None):
        if type(message) == dict:
            super(GenericException, self).__init__()
            self.dict_detail = message
        else:
            super(GenericException, self).__init__(message)
