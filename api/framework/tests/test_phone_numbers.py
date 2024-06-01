import mock
import phonenumbers
from django.test import TestCase
from api.framework.phone_numbers import PhoneNumber, InvalidPhoneNumber


class TestPhoneNumber(TestCase):
    def setUp(self):
        self.number = PhoneNumber('+1 (202) 555-0104')

    def test_format(self):
        number = PhoneNumber('+1 (202) 555-0104', format_name='E164')
        self.assertEqual(number.format, phonenumbers.PhoneNumberFormat.E164)

    def test_invalid_format(self):
        number = PhoneNumber('+1 (202) 555-0104', format_name='INVALID')
        self.assertEqual(number.format, None)

    def test_number(self):
        number = PhoneNumber('+1 (202) 555-0104', default_region='US')
        self.assertEqual(number.raw_number, '+1 (202) 555-0104')
        self.assertEqual(number.number, phonenumbers.parse('+1 (202) 555-0104', 'US'))

    def test_invalid_number(self):
        with self.assertRaises(InvalidPhoneNumber):
            PhoneNumber('abcde', default_region='US')

    @mock.patch('phonenumbers.is_valid_number', return_value=True)
    def test_is_valid(self, mock_is_valid_number):
        self.assertTrue(self.number.is_valid())

    @mock.patch('phonenumbers.is_valid_number', return_value=False)
    def test_is_invalid(self, mock_is_valid_number):
        self.assertFalse(self.number.is_valid())

    @mock.patch('phonenumbers.format_number', return_value='+12025550104')
    def test_cleaned(self, mock_format_number):
        self.assertEqual(self.number.cleaned(), '+12025550104')

    @mock.patch('phonenumbers.format_number', return_value='+12025550104')
    def test_str(self, mock_format_number):
        self.assertEqual(str(self.number), '+12025550104')
