from django.test import TestCase

from api.framework.generics import GenericAPIView


class TestGetQueryParamsSerializerClass(TestCase):
    def setUp(self):
        self.view = GenericAPIView()

    def test_get_query_params_serializer_class_w_no_query_params_serializer_class(self):
        serializer_class = self.view.get_query_params_serializer_class()
        self.assertEqual(serializer_class, None)

    def test_get_query_params_serializer_class(self):
        self.view.query_params_serializer_class = 'serializer_class'

        serializer_class = self.view.get_query_params_serializer_class()
        self.assertEqual(serializer_class, 'serializer_class')
