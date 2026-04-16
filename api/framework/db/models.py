from django.db.models import *  # noqa
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _

class Model(Model):
    class Meta:
        abstract = True

    class ValidationError(APIException):
        """
        Raised when an error occurs during the creation of an availability.
        """
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        default_detail = _('An error occurred while validating the model.')
        default_code = 'validation_error'

        def __init__(self, detail=None, code=None):
            if detail is None:
                detail = self.default_detail
            if code is None:
                code = self.default_code
            if isinstance(detail, list):
                # Store list as-is so None slots survive; DRF's _get_error_details
                # would turn None into the string 'None' via force_str().
                self.detail = detail
            else:
                super().__init__(detail, code)

        def get_full_details(self):
            if isinstance(self.detail, list):
                # Return the list directly; items are already plain dicts or None,
                # not ErrorDetail objects that need code/message extraction.
                return self.detail
            return super().get_full_details()

    def is_valid(self, raise_exception: bool = False):
        """
        Determines whether the current instance or configuration is valid.

        This method performs a validation check and returns a boolean based on
        the validity of the instance or configuration being evaluated. Optionally,
        it can raise an exception if the instance is not valid by enabling the
        `raise_exception` parameter. Specific validation logic is implemented
        within the method.

        Args:
            raise_exception (bool): A flag indicating whether to raise an exception
                if the instance is found to be invalid. Defaults to False.

        Returns:
            bool: True if the instance is valid; otherwise, False.
        """
        return True

    def save(self, *args, **kwargs):
        """
        Saves the current model instance after performing validation.

        This method first validates the instance by calling `is_valid` with
        `raise_exception=True`. If the validation passes, it proceeds to save
        the instance to the database using the parent class's save method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.is_valid(raise_exception=True)
        super().save(*args, **kwargs)