import phonenumbers
from rest_framework.serializers import *  # noqa

from api.framework.phone_numbers import PhoneNumber
from django.utils.translation import gettext_lazy as _


class Serializer(Serializer):
    @property
    def request(self):
        return self.context['request']


class PhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _('"{value}" is not a valid phone number.')
    }

    def to_internal_value(self, data):
        try:
            number = PhoneNumber(data)
        except phonenumbers.phonenumberutil.NumberParseException:
            self.fail('invalid', value=data)
        else:
            if number.is_valid():
                return number.cleaned()

            self.fail('invalid', value=data)
