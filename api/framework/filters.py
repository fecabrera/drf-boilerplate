from django.utils.translation import gettext_lazy as _
from rest_framework import filters


class GenericFilterBackend(filters.BaseFilterBackend):
    lookup_field = None
    lookup_expr = None
    lookup_value = None

    def get_lookup_field(self, **kwargs):
        return self.lookup_field

    def get_lookup_expr(self, **kwargs):
        return self.lookup_expr

    def get_lookup_value(self, **kwargs):
        return self.lookup_value

    def get_lookup_kwargs(self, lookup_field, lookup_expr, lookup_value):
        assert lookup_field is not None, _('`{value}` must be set').format(value='lookup_field')

        if lookup_expr is not None:
            lookup_field = f'{lookup_field}__{lookup_expr}'

        return {lookup_field: lookup_value}

    def apply_filter(self, queryset, lookup_field, lookup_expr, lookup_value):
        lookup_kwargs = self.get_lookup_kwargs(lookup_field, lookup_expr, lookup_value)
        return queryset.filter(**lookup_kwargs)

    def filter_queryset(self, request, queryset, view):
        lookup_field = self.get_lookup_field(request=request, view=view)
        lookup_expr = self.get_lookup_expr(request=request, view=view)
        lookup_value = self.get_lookup_value(request=request, view=view)
        return self.apply_filter(queryset, lookup_field, lookup_expr, lookup_value)

