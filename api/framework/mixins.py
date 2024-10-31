from rest_framework.mixins import *  # noqa


class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        query_params = self.get_query_params_serializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        self.query_params = query_params.validated_data

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)