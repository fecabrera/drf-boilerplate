from unittest import mock
from unittest.mock import MagicMock
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.test import TestCase

# filters
from api.framework.filters import GenericFilterBackend


class TestGenericFilterBackend(TestCase):
    def setUp(self):
        self.queryset = MagicMock(spec=QuerySet)
        self.filter = GenericFilterBackend()

    def test_get_lookup_kwargs(self):
        lookup_kwargs = self.filter.get_lookup_kwargs(
            lookup_field='field',
            lookup_expr='expr',
            lookup_value='value',
        )
        self.assertEqual(lookup_kwargs, {'field__expr': 'value'})

    def test_get_lookup_kwargs_wo_lookup_expr(self):
        lookup_kwargs = self.filter.get_lookup_kwargs(
            lookup_field='field',
            lookup_expr=None,
            lookup_value='value',
        )
        self.assertEqual(lookup_kwargs, {'field': 'value'})

    def test_get_lookup_kwargs_wo_lookup_field(self):
        with self.assertRaisesMessage(AssertionError, _('`{value}` must be set').format(value='lookup_field')):
            self.filter.get_lookup_kwargs(
                lookup_field=None,
                lookup_expr='expr',
                lookup_value='value',
            )

    def test_get_lookup_kwargs_wo_lookup_value(self):
        lookup_kwargs = self.filter.get_lookup_kwargs(
            lookup_field='field',
            lookup_expr='expr',
            lookup_value=None,
        )
        self.assertEqual(lookup_kwargs, {'field__expr': None})

    def test_get_lookup_kwargs_wo_lookup_expr_value(self):
        lookup_kwargs = self.filter.get_lookup_kwargs(
            lookup_field='field',
            lookup_expr=None,
            lookup_value=None,
        )
        self.assertEqual(lookup_kwargs, {'field': None})

    @mock.patch.object(GenericFilterBackend, 'get_lookup_kwargs')
    def test_apply_filter(self, mock_get_lookup_kwargs):
        mock_get_lookup_kwargs.return_value = {'key': 'value'}

        self.filter.apply_filter(self.queryset, 'field', 'expr', 'value')

        self.queryset.filter.assert_called_once_with(key='value')
        mock_get_lookup_kwargs.assert_called_once_with('field', 'expr', 'value')

    @mock.patch.object(GenericFilterBackend, 'apply_filter')
    def test_filter_queryset(self, mock_apply_filter):
        self.filter.filter_queryset(None, self.queryset, None)

        mock_apply_filter.assert_called_once_with(self.queryset, None, None, None)

    @mock.patch.object(GenericFilterBackend, 'get_lookup_field')
    @mock.patch.object(GenericFilterBackend, 'get_lookup_expr')
    @mock.patch.object(GenericFilterBackend, 'get_lookup_value')
    @mock.patch.object(GenericFilterBackend, 'apply_filter')
    def test_filter_queryset_w_values(self, mock_apply_filter, mock_get_lookup_value, mock_get_lookup_expr, mock_get_lookup_field):
        mock_get_lookup_field.return_value = 'field'
        mock_get_lookup_expr.return_value = 'expr'
        mock_get_lookup_value.return_value = 'value'

        self.filter.filter_queryset(None, self.queryset, None)

        mock_apply_filter.assert_called_once_with(self.queryset, 'field', 'expr', 'value')
