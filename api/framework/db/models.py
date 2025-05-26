from django.db.models import *  # noqa


class Model(Model):
    class Meta:
        abstract = True

    class ValidationError(Exception):
        """
        Raised when an error occurs during the creation of an availability.
        """
        pass

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