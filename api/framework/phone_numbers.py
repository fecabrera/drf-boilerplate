import phonenumbers
from django.conf import settings


class PhoneNumber(object):
    format = phonenumbers.PhoneNumberFormat.E164

    def __init__(self, value, default_region=None, format_name=None):
        if default_region is None:
            default_region = settings.PHONE_NUMBER_DEFAULT_REGION

        if format_name:
            self.format = getattr(phonenumbers.PhoneNumberFormat, format_name, None)

        self.raw_number = value
        self.number = phonenumbers.parse(value, default_region)

    def is_valid(self):
        return phonenumbers.is_valid_number(self.number)

    def cleaned(self):
        return phonenumbers.format_number(self.number, self.format)

    def __str__(self):
        return self.cleaned()
