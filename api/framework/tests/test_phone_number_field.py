import mock
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.framework.phone_numbers import InvalidPhoneNumber
from api.framework.serializers import PhoneNumberField


class TestPhoneNumberField(TestCase):
    def setUp(self):
        self.field = PhoneNumberField()

    @mock.patch('phonenumbers.format_number', return_value='+12025550104')
    def test_to_internal_value(self, mock_format_number):
        value = self.field.to_internal_value('+1 (202) 555-0104')
        self.assertEqual(value, '+12025550104')

    @mock.patch('api.framework.serializers.PhoneNumber', side_effect=InvalidPhoneNumber)
    def test_to_internal_value_fail(self, mock_phone_number):
        with self.assertRaises(ValidationError) as e:
            self.field.to_internal_value('invalid')
        self.assertEqual(e.exception.detail, [_('"{value}" is not a valid phone number.').format(value='invalid')])

    @mock.patch('api.framework.serializers.PhoneNumber.is_valid', return_value=False)
    def test_to_internal_value_invalid(self, mock_is_valid):
        with self.assertRaises(ValidationError) as e:
            self.field.to_internal_value('+1 (123) 456-7890')
        self.assertEqual(e.exception.detail, [_('"{value}" is not a valid phone number.').format(value='+1 (123) 456-7890')])
