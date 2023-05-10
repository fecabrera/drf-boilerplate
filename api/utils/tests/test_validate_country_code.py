from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.utils.validators import validate_country_code


class TestValidateCountryCode(APITestCase):
    def test_validate_country_code(self):
        self.assertEqual(validate_country_code('US'), 'US')
        self.assertEqual(validate_country_code('CA'), 'CA')
        self.assertEqual(validate_country_code('Cl'), 'CL')

    def test_validate_country_code_lowercase(self):
        self.assertEqual(validate_country_code('us'), 'US')
        self.assertEqual(validate_country_code('cA'), 'CA')
        self.assertEqual(validate_country_code('CL'), 'CL')

    def test_validate_country_code_invalid(self):
        with self.assertRaises(ValidationError) as e:
            validate_country_code('XX')
            self.assertEqual(e.exception.detail, _('Invalid country code.'))
