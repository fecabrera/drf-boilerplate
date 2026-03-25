from django.test import TestCase
from api.framework.serializers import ChoiceDisplayField
from django.db import models

class TestIntegerChoices(models.IntegerChoices):
    ONE = (1, 'One')
    TWO = (2, 'Two')
    THREE = (3, 'Three')


class TestStringChoices(models.TextChoices):
    ONE = ('one', 'One')
    TWO = ('two', 'Two')
    THREE = ('three', 'Three')


class TestChoiceDisplayField(TestCase):
    def setUp(self):
        self.integer_field = ChoiceDisplayField(choices=TestIntegerChoices.choices)
        self.string_field = ChoiceDisplayField(choices=TestStringChoices.choices)

    def test_to_representation(self):
        self.assertEqual(self.integer_field.to_representation(1), 'One')
        self.assertEqual(self.integer_field.to_representation(2), 'Two')
        self.assertEqual(self.integer_field.to_representation(3), 'Three')

        self.assertEqual(self.string_field.to_representation('one'), 'One')
        self.assertEqual(self.string_field.to_representation('two'), 'Two')
        self.assertEqual(self.string_field.to_representation('three'), 'Three')
