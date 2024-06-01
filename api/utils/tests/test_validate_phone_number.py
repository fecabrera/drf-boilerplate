import mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.framework.phone_numbers import InvalidPhoneNumber
from api.utils.validators import validate_phone_number


class TestValidatePhoneNumber(TestCase):
    @mock.patch('phonenumbers.is_valid_number', return_value=True)
    def test_validate_phone_number(self, mock_is_valid_number):
        validate_phone_number('+12025550104')

    @mock.patch('phonenumbers.is_valid_number', return_value=True)
    def test_validate_phone_number_not_clean(self, mock_is_valid_number):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('+1 202-555-0104')
        self.assertEqual(e.exception.message, _('Invalid phone number.'))

    @mock.patch('phonenumbers.is_valid_number', return_value=False)
    def test_validate_phone_number_invalid(self, mock_is_valid_number):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('+1 202-555-0104')
        self.assertEqual(e.exception.message, _('Invalid phone number.'))

    @mock.patch('phonenumbers.parse', side_effect=InvalidPhoneNumber)
    def test_validate_phone_number_wrong_format(self, mock_parse):
        with self.assertRaises(ValidationError) as e:
            validate_phone_number('202-555-0104')
        self.assertEqual(e.exception.message, _('Invalid phone number.'))
