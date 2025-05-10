from rest_framework.mixins import *  # noqa


class ListModelMixin(ListModelMixin):
    """
    List a queryset.
    """
    query_params = None

    def list(self, request, *args, **kwargs):
        query_params = self.get_query_params_serializer(data=request.query_params)

        if query_params is not None:
            query_params.is_valid(raise_exception=True)
            self.query_params = query_params.validated_data

        return super().list(request, *args, **kwargs)
