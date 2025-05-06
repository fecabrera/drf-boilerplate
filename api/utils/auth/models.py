import pyotp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


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


class OTPBase(models.Model):
    class Meta:
        abstract = True

    otp_secret = models.CharField(_('otp secret'), max_length=32)
    verified = models.BooleanField(_('verified'), default=False)

    def generate(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()

        self.verified = False
        self.save()

        totp = pyotp.TOTP(self.otp_secret, interval=300)
        return totp.now()

    def verify(self, otp_code):
        totp = pyotp.TOTP(self.otp_secret, interval=300)
        verified = totp.verify(otp_code, valid_window=1)
        self.verified = verified
        self.save()
        return verified
