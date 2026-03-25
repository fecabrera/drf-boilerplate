from unittest import mock
from unittest.mock import MagicMock
from django.test import TestCase
from django.db.models import QuerySet
from rest_framework.request import Request
from api.framework.generics import GenericAPIView


class TestGetObject(TestCase):
    def setUp(self):
        self.queryset = MagicMock(spec=QuerySet)
        self.view = GenericAPIView()
        self.view.get_queryset = lambda: self.queryset
        self.view.filter_queryset = lambda qs: qs
        self.view.kwargs = {}
        self.view.request = MagicMock(spec=Request, query_params={'pk': 1})

    @mock.patch.object(GenericAPIView, 'check_object_permissions')
    def test_get_object_w_no_pk(self, mock_check_object_permissions):
        with self.assertRaises(AssertionError):
            self.view.get_object()

    @mock.patch.object(GenericAPIView, 'check_object_permissions')
    def test_get_object(self, mock_check_object_permissions):
        self.view.kwargs['pk'] = 1
        self.assertEqual(self.view.get_object(), self.queryset.get())
