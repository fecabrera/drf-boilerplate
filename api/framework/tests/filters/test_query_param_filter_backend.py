from unittest import mock
from unittest.mock import MagicMock
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from django.views import View

# filters
from api.framework.filters import QueryParamFilterBackend


class TestQueryParamFilterBackend(TestCase):
    def setUp(self):
        self.queryset = MagicMock(spec=QuerySet)
        self.view = MagicMock(spec=View)
        self.filter = QueryParamFilterBackend()

    def test_get_lookup_value_w_no_lookup_value(self):
        with self.assertRaisesMessage(AssertionError, _('`{value}` must be set').format(value='lookup_value')):
            self.filter.get_lookup_value(None, self.view)

    def test_get_lookup_value(self):
        self.filter.lookup_value = 'key'
        self.view.query_params = {}
        lookup_value = self.filter.get_lookup_value(None, self.view)
        self.assertEqual(lookup_value, None)

    def test_get_lookup_value_w_value(self):
        self.filter.lookup_value = 'key'
        self.view.query_params = {'key': 'value'}
        lookup_value = self.filter.get_lookup_value(None, self.view)
        self.assertEqual(lookup_value, 'value')

    @mock.patch.object(QueryParamFilterBackend, 'get_lookup_kwargs')
    def test_apply_filter(self, mock_get_lookup_kwargs):
        mock_get_lookup_kwargs.return_value = {'key': 'value'}

        self.filter.apply_filter(self.queryset, 'field', 'expr', None)

        self.queryset.filter.assert_not_called()
        mock_get_lookup_kwargs.assert_not_called()

    @mock.patch.object(QueryParamFilterBackend, 'get_lookup_kwargs')
    def test_apply_filter_w_lookup_value(self, mock_get_lookup_kwargs):
        mock_get_lookup_kwargs.return_value = {'key': 'value'}

        self.filter.apply_filter(self.queryset, 'field', 'expr', 'value')

        self.queryset.filter.assert_called_once_with(key='value')
        mock_get_lookup_kwargs.assert_called_once_with('field', 'expr', 'value')

