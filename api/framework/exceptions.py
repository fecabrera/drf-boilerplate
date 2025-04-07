from rest_framework.exceptions import *  # noqa
from django.utils.translation import gettext_lazy as _


class AlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Already exists.')
    default_code = 'already_exists'
