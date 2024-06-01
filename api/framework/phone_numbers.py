import phonenumbers
from django.conf import settings


class InvalidPhoneNumber(Exception):
    pass


class PhoneNumber(object):
    _default_region = settings.PHONE_NUMBER_DEFAULT_REGION
    _format = phonenumbers.PhoneNumberFormat.E164
    _raw_number: str
    _number: phonenumbers.PhoneNumber

    def __init__(self, value, default_region=None, format_name=None):
        if default_region:
            self._default_region = default_region
        if format_name:
            self._format = getattr(phonenumbers.PhoneNumberFormat, format_name, None)

        self.number = value

    @property
    def format(self):
        return self._format

    @property
    def raw_number(self):
        return self._raw_number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        try:
            self._raw_number = value
            self._number = phonenumbers.parse(value, self._default_region)
        except phonenumbers.NumberParseException:
            raise InvalidPhoneNumber()

    def is_valid(self):
        return phonenumbers.is_valid_number(self.number)

    def cleaned(self):
        return phonenumbers.format_number(self.number, self.format)

    def __str__(self):
        return self.cleaned()
