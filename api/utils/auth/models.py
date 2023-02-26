from api.utils.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    class Meta:
        abstract = True
