import pycountry
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from api.framework.phone_numbers import PhoneNumber, InvalidPhoneNumber


def validate_country_code(value):
    country = pycountry.countries.get(alpha_2=value)

    if not country:
        raise ValidationError(_("Invalid country code."))


def validate_phone_number(value):
    try:
        number = PhoneNumber(value)
    except InvalidPhoneNumber:
        raise ValidationError(_("Invalid phone number."))

    if not number.is_valid():
        raise ValidationError(_("Invalid phone number."))

    if value != number.cleaned():
        raise ValidationError(_("Invalid phone number."))
