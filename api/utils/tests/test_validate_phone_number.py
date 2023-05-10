import mock
from phonenumbers import NumberParseException
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.utils.validators import validate_phone_number


class TestValidatePhoneNumber(APITestCase):
    @mock.patch('phonenumbers.is_valid_number', return_value=True)
    def test_validate_phone_number(self, mock_is_valid_number):
        validate_phone_number('+12025550104')

    @mock.patch('phonenumbers.is_valid_number', return_value=True)
    def test_validate_phone_number_not_clean(self, mock_is_valid_number):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('+1 202-555-0104')
            self.assertEqual(e.exception.detail, _('Invalid phone number.'))

    @mock.patch('phonenumbers.is_valid_number', return_value=False)
    def test_validate_phone_number_invalid(self, mock_is_valid_number):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('+1 202-555-0104')
            self.assertEqual(e.exception.detail, _('Invalid phone number.'))

    @mock.patch('phonenumbers.parse', side_effect=NumberParseException(NumberParseException.NOT_A_NUMBER, _('The string supplied did not seem to be a phone number.')))
    def test_validate_phone_number_wrong_format(self, mock_parse):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('202-555-0104')
            self.assertEqual(e.exception.detail, _('Invalid phone number.'))
