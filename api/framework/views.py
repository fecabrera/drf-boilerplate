from django.db.models import QuerySet
from rest_framework.views import *  # noqa


class APIView(APIView):
    queryset = None
    serializer_class = None
    query_params_serializer_class = None

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        """
        Get the serializer class for this view.
        Defaults to using `self.serializer_class`.

        This method should always be used rather than accessing `self.serializer_class`
        directly, as this is used by the `get_serializer()` method.

        You may want to override this if you need to provide different
        serializer classes depending on the incoming request.
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
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

    def get_query_params_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_query_params_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
