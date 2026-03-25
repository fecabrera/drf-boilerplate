from unittest import mock
from django.test import TestCase
from api.framework.db.functions import BinaryFunc


class TestBinaryFunc(TestCase):
    def setUp(self):
        self.compiler = mock.MagicMock(compile=lambda x: (x, []))

    def test_as_sql_no_function(self):
        self.func = BinaryFunc('1', '2')
        with self.assertRaisesMessage(
            AssertionError,
            "BinaryFunc should either include a `function` attribute, or pass it as an argument when calling `as_sql()`."
        ):
            self.func.as_sql(self.compiler, None)

    def test_as_sql(self):
        self.func = BinaryFunc('1', '2')
        self.func.function = '+'
        self.assertEqual(self.func.as_sql(self.compiler, None), ('F(1) + F(2)', []))

    def test_as_sql_w_function(self):
        self.func = BinaryFunc('1', '2')
        self.assertEqual(self.func.as_sql(self.compiler, None, function='+'), ('F(1) + F(2)', []))
