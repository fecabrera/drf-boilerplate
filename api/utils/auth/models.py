import pyotp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseUser(AbstractBaseUser, PermissionsMixin):  # pragma: no cover
    email = models.EmailField(_('email'), unique=True, db_index=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active status'), default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    class Meta:
        abstract = True


class OTPBase(models.Model):  # pragma: no cover
    class Meta:
        abstract = True

    TOTP_INTERVAL = None

    otp_secret = models.CharField(_('otp secret'), max_length=32)
    generated_at = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(_('verified'), default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate(self) -> str:
        """
        Generates a new OTP code and returns it.

        Returns:
            str: The OTP code.
        """
        assert self.TOTP_INTERVAL is not None, _('`{value}` must be set').format(value='TOTP_INTERVAL')

        if not self.generated_at:
            self.otp_secret = pyotp.random_base32()
            self.generated_at = timezone.now()

        self.verified = False
        self.verified_at = None
        self.used_at = None
        self.save()

        totp = pyotp.TOTP(self.otp_secret, interval=self.TOTP_INTERVAL)
        return totp.now()

    def verify(self, otp_code: str) -> bool:
        """
        Verifies the OTP code and returns True if it is valid, False otherwise.

        Args:
            otp_code: The OTP code to verify.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        assert self.TOTP_INTERVAL is not None, _('`{value}` must be set').format(value='TOTP_INTERVAL')
        assert self.generated_at is not None, _('This OTP is not generated.')
        assert self.verified_at is None, _('This OTP has already been verified.')
        assert self.used_at is None, _('This OTP has already been used.')

        totp = pyotp.TOTP(self.otp_secret, interval=self.TOTP_INTERVAL)
        verified = totp.verify(otp_code, valid_window=1)
        self.verified = verified
        self.verified_at = timezone.now() if verified else None
        self.save()
        return verified
    
    def use(self) -> None:
        """
        Marks the OTP code as used by setting the used_at field to the current time.

        Raises:
            AssertionError: If the OTP code is not verified.
            AssertionError: If the OTP code has already been used.
        """
        assert self.used_at is None, _('This OTP has already been used.')
        assert self.verified_at is not None, _('This OTP is not verified.')
        assert self.generated_at is not None, _('This OTP is not generated.')

        self.used_at = timezone.now()
        self.save()