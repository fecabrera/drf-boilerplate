from rest_framework.serializers import *  # noqa
from django.utils.translation import gettext_lazy as _
from api.framework.phone_numbers import PhoneNumber, InvalidPhoneNumber


class RequestMixin:
    @property
    def request(self):
        assert 'request' in self.context, (
            "'%s' should be instantiated with a request in the context."
            % self.__class__.__name__
        )

        return self.context['request']

    @property
    def format(self):
        assert 'format' in self.context, (
            "'%s' should be instantiated with a format in the context."
            % self.__class__.__name__
        )

        return self.context['format']

    @property
    def view(self):
        assert 'view' in self.context, (
            "'%s' should be instantiated with a view in the context."
            % self.__class__.__name__
        )

        return self.context['view']


class Serializer(Serializer, RequestMixin):
    pass


class ModelSerializer(ModelSerializer, RequestMixin):
    pass


class PhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _('"{value}" is not a valid phone number.')
    }

    def to_internal_value(self, data):
        try:
            number = PhoneNumber(data)
        except InvalidPhoneNumber:
            self.fail('invalid', value=data)
        else:
            if number.is_valid():
                return number.cleaned()

            self.fail('invalid', value=data)
