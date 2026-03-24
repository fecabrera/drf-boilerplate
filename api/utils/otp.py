from django.conf import settings
from rest_framework.response import Response
from api.utils.auth.models import OTPBase


def set_otp_secret_cookie(response: Response, otp: OTPBase):
    """
    Sets the otp_secret as a short-lived, HTTP-Only cookie.

    Args:
        response: The response object to set the cookie on.
        otp: The OTP object to set the cookie for.
    """
    response.set_cookie(
        'otp_secret',
        otp.otp_secret,
        path='/',
        httponly=True,
        secure=settings.OTP_SECRET_COOKIE_SECURE,
        max_age=otp.TOTP_INTERVAL,
        samesite=settings.OTP_SECRET_COOKIE_SAMESITE,
        domain=settings.OTP_SECRET_COOKIE_DOMAIN,
    )
