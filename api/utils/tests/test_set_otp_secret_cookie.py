from django.test import TestCase, override_settings
from unittest.mock import Mock
from rest_framework.response import Response
from api.utils.auth.models import OTPBase
from api.utils.otp import set_otp_secret_cookie


class TestSetOtpSecretCookie(TestCase):
    def setUp(self):
        self.response = Response()
        self.otp = Mock(spec=OTPBase, otp_secret='secret', TOTP_INTERVAL=300)

    @override_settings(
        OTP_SECRET_COOKIE_SAMESITE='Lax',
        OTP_SECRET_COOKIE_DOMAIN='localhost',
    )
    def test_set_otp_secret_cookie(self):
        set_otp_secret_cookie(self.response, self.otp)
        otp_secret_cookie = self.response.cookies['otp_secret']
        self.assertEqual(otp_secret_cookie.value, self.otp.otp_secret)
        self.assertEqual(otp_secret_cookie['path'], '/')
        self.assertEqual(otp_secret_cookie['httponly'], True)
        self.assertEqual(otp_secret_cookie['max-age'], self.otp.TOTP_INTERVAL)
        self.assertEqual(otp_secret_cookie['secure'], True)
        self.assertEqual(otp_secret_cookie['samesite'], 'Lax')
        self.assertEqual(otp_secret_cookie['domain'], 'localhost')
    
    @override_settings(
        OTP_SECRET_COOKIE_SAMESITE='Strict',
        OTP_SECRET_COOKIE_DOMAIN='example.com',
    )
    def test_set_otp_secret_cookie_samesite_strict_domain_different(self):
        set_otp_secret_cookie(self.response, self.otp)
        otp_secret_cookie = self.response.cookies['otp_secret']
        self.assertEqual(otp_secret_cookie.value, self.otp.otp_secret)
        self.assertEqual(otp_secret_cookie['path'], '/')
        self.assertEqual(otp_secret_cookie['httponly'], True)
        self.assertEqual(otp_secret_cookie['max-age'], self.otp.TOTP_INTERVAL)
        self.assertEqual(otp_secret_cookie['secure'], True)
        self.assertEqual(otp_secret_cookie['samesite'], 'Strict')
        self.assertEqual(otp_secret_cookie['domain'], 'example.com')
