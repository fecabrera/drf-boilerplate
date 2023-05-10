from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_country_code(value):
    import pycountry

    country = pycountry.countries.get(alpha_2=value)

    if not country:
        raise ValidationError(_("Invalid country code."))

    return country.alpha_2


def validate_phone_number(value):
    import phonenumbers

    try:
        number = phonenumbers.parse(value, settings.PHONE_NUMBER_DEFAULT_REGION)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(_("Invalid phone number."))

    if not phonenumbers.is_valid_number(number):
        raise ValidationError(_("Invalid phone number."))

    return str(number.country_code) + str(number.national_number)
