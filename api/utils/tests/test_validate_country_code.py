from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.utils.validators import validate_country_code


class TestValidateCountryCode(TestCase):
    def test_validate_country_code(self):
        validate_country_code('US')
        validate_country_code('CA')
        validate_country_code('Cl')

    def test_validate_country_code_lowercase(self):
        validate_country_code('us')
        validate_country_code('cA')
        validate_country_code('CL')

    def test_validate_country_code_invalid(self):
        with self.assertRaises(ValidationError) as e:
            validate_country_code('XX')
            self.assertEqual(e.exception.detail, _('Invalid country code.'))
