from unittest import mock
from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework.request import Request

from api.framework.generics import GenericAPIView
from api.framework import serializers


class TestGenericAPIView(TestCase):
    def setUp(self):
        self.view = GenericAPIView()
        self.request = MagicMock(spec=Request)
        self.serializer = MagicMock(spec=serializers.Serializer)
        self.serializer_class = MagicMock(return_value=self.serializer)

    def test_get_query_params_serializer_class_w_no_query_params_serializer_class(self):
        serializer_class = self.view.get_query_params_serializer_class()
        self.assertEqual(serializer_class, None)

    def test_get_query_params_serializer_class(self):
        self.view.query_params_serializer_class = 'serializer_class'

        serializer_class = self.view.get_query_params_serializer_class()
        self.assertEqual(serializer_class, 'serializer_class')

    @mock.patch.object(GenericAPIView, 'get_query_params_serializer_class')
    @mock.patch.object(GenericAPIView, 'get_serializer_context')
    def test_get_query_params_serializer_w_no_query_params_serializer_class(self, mock_get_serializer_context, mock_get_query_params_serializer_class):
        mock_get_query_params_serializer_class.return_value = None
        mock_get_serializer_context.return_value = {'context': 'value'}

        args = ('arg',)
        kwargs = {'key': 'value'}
        serializer = self.view.get_query_params_serializer(*args, **kwargs)
        self.assertEqual(serializer, None)

        mock_get_query_params_serializer_class.assert_called_once()
        mock_get_serializer_context.assert_not_called()
        self.serializer_class.assert_not_called()

    @mock.patch.object(GenericAPIView, 'get_query_params_serializer_class')
    @mock.patch.object(GenericAPIView, 'get_serializer_context')
    def test_get_query_params_serializer(self, mock_get_serializer_context, mock_get_query_params_serializer_class):
        mock_get_query_params_serializer_class.return_value = self.serializer_class
        mock_get_serializer_context.return_value = {'context': 'value'}

        args = ('arg',)
        kwargs = {'key': 'value'}
        serializer = self.view.get_query_params_serializer(*args, **kwargs)
        self.assertEqual(serializer, self.serializer)

        mock_get_query_params_serializer_class.assert_called_once()
        mock_get_serializer_context.assert_called_once()
        self.serializer_class.assert_called_once_with(*args, context={'context': 'value'}, **kwargs)