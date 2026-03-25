from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework import status
from rest_framework.request import Request
from api.framework.mixins import BatchCreateModelMixin
from api.framework.serializers import Serializer


class TestBatchCreateModelMixin(TestCase):
    def setUp(self):
        self.request = MagicMock(spec=Request)
        self.serializer = MagicMock(spec=Serializer, data=[{'field': 'value'}])

        self.mixin = BatchCreateModelMixin()
        self.mixin.get_serializer = MagicMock(return_value=self.serializer)
        self.mixin.get_success_headers = MagicMock(return_value={'Location': 'http://test.com'})
    
    def test_create(self):
        response = self.mixin.create(self.request)
        self.assertEqual(response.data, [{'field': 'value'}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.headers['Location'], 'http://test.com')

        self.mixin.get_serializer.assert_called_once_with(data=self.request.data, many=True, allow_empty=False)
