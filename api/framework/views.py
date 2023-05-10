from rest_framework.views import *  # noqa


class APIView(APIView):
    serializer_class = None

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request
        }
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)
