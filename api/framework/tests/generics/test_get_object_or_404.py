from unittest import mock
from unittest.mock import MagicMock
from django.http import Http404
from django.test import TestCase
from django.core.exceptions import ValidationError

from api.framework.generics import get_object_or_404

class TestGetObjectOr404(TestCase):
    @mock.patch('api.framework.generics._get_object_or_404', return_value='mocked_object')
    def test_get_object_or_404(self, mock_get_object_or_404):
        queryset = MagicMock()
        args = (1,)
        kwargs = {'id': 1}

        obj = get_object_or_404(queryset, *args, **kwargs)
        self.assertEqual(obj, 'mocked_object')

        mock_get_object_or_404.assert_called_once_with(queryset, *args, **kwargs)

    @mock.patch('api.framework.generics._get_object_or_404', side_effect=TypeError)
    def test_get_object_or_404_w_type_error(self, mock_get_object_or_404):
        queryset = MagicMock()
        args = (1,)
        kwargs = {'id': 1}

        with self.assertRaises(Http404):
            get_object_or_404(queryset, *args, **kwargs)

        mock_get_object_or_404.assert_called_once_with(queryset, *args, **kwargs)

    @mock.patch('api.framework.generics._get_object_or_404', side_effect=ValueError)
    def test_get_object_or_404_w_value_error(self, mock_get_object_or_404):
        queryset = MagicMock()
        args = (1,)
        kwargs = {'id': 1}

        with self.assertRaises(Http404):
            get_object_or_404(queryset, *args, **kwargs)

        mock_get_object_or_404.assert_called_once_with(queryset, *args, **kwargs)

    @mock.patch('api.framework.generics._get_object_or_404', side_effect=ValidationError)
    def test_get_object_or_404_w_validation_error(self, mock_get_object_or_404):
        queryset = MagicMock()
        args = (1,)
        kwargs = {'id': 1}

        with self.assertRaises(Http404):
            get_object_or_404(queryset, *args, **kwargs)

        mock_get_object_or_404.assert_called_once_with(queryset, *args, **kwargs)
