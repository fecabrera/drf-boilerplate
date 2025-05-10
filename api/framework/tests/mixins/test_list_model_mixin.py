from unittest import mock
from unittest.mock import MagicMock
from django.test import TestCase

# mixins
from rest_framework.mixins import ListModelMixin as _ListModelMixin
from rest_framework.request import Request

from api.framework.mixins import ListModelMixin
from api.framework.serializers import Serializer


class TestListModelMixin(TestCase):
    def setUp(self):
        self.request = MagicMock(spec=Request, query_params={'object_id': '1'})
        self.serializer = MagicMock(spec=Serializer, validated_data={'object_id': 1})
        self.get_query_params_serializer = MagicMock()

        self.mixin = ListModelMixin()
        self.mixin.get_query_params_serializer = self.get_query_params_serializer

    @mock.patch.object(_ListModelMixin, 'list', return_value='response')
    def test_list_model_mixin(self, mock_list):
        self.get_query_params_serializer.return_value = None

        response = self.mixin.list(self.request)
        self.assertEqual(response, 'response')
        self.assertEqual(self.mixin.query_params, None)

        self.mixin.get_query_params_serializer.assert_called_once_with(data=self.request.query_params)
        self.serializer.is_valid.assert_not_called()
        mock_list.assert_called_once_with(self.request)

    @mock.patch.object(_ListModelMixin, 'list', return_value='response')
    def test_list_model_mixin_w_query_params(self, mock_list):
        self.get_query_params_serializer.return_value = self.serializer

        response = self.mixin.list(self.request)
        self.assertEqual(response, 'response')
        self.assertEqual(self.mixin.query_params, {'object_id': 1})

        self.mixin.get_query_params_serializer.assert_called_once_with(data=self.request.query_params)
        self.serializer.is_valid.assert_called_once_with(raise_exception=True)
        mock_list.assert_called_once_with(self.request)
