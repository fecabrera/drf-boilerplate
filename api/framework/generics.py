from rest_framework.generics import *  # noqa


class GenericAPIView(GenericAPIView):
    query_params_serializer_class = None

    def get_query_params_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_query_params_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_query_params_serializer_class(self):
        """
        Return the class to use for the query params serializer.
        Defaults to using `self.query_params_serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.query_params_serializer_class is not None, (
            "'%s' should either include a `query_params_serializer_class` attribute, "
            "or override the `get_query_params_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.query_params_serializer_class
