from django.test import TestCase

from api.framework.serializers import Serializer


class TestSerializers(TestCase):
    def test_serializer_context_not_provided(self):
        serializer = Serializer()

        with self.assertRaises(AssertionError):
            _ = serializer.request

        with self.assertRaises(AssertionError):
            _ = serializer.format

        with self.assertRaises(AssertionError):
            _ = serializer.view

    def test_serializer_context_empty(self):
        serializer = Serializer(context={})

        with self.assertRaises(AssertionError):
            _ = serializer.request

        with self.assertRaises(AssertionError):
            _ = serializer.format

        with self.assertRaises(AssertionError):
            _ = serializer.view

    def test_serializer_context(self):
        context = {
            'request': 'request',
            'format': 'format',
            'view': 'view'
        }

        serializer = Serializer(context=context)

        self.assertEqual(serializer.request, context['request'])
        self.assertEqual(serializer.format, context['format'])
        self.assertEqual(serializer.view, context['view'])