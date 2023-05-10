from rest_framework.serializers import *  # noqa


class Serializer(Serializer):
    @property
    def request(self):
        return self.context['request']
