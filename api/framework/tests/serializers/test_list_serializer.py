from unittest.mock import MagicMock

from django.test import TestCase

from api.framework.db.models import Model
from api.framework.serializers import ListSerializer


class _ChildMetaModel:
    """Minimal stand-in for ``child.Meta.model``; only ``ValidationError`` is used."""
    ValidationError = Model.ValidationError


class TestListSerializer(TestCase):
    def test_create_returns_instances_when_all_succeed(self):
        child = MagicMock()
        child.Meta.model = _ChildMetaModel
        child.create.side_effect = ['first', 'second']

        serializer = ListSerializer(child=child)
        result = serializer.create([{'a': 1}, {'b': 2}])

        self.assertEqual(result, ['first', 'second'])
        self.assertEqual(child.create.call_count, 2)

    def test_create_raises_detail_when_first_item_fails(self):
        child = MagicMock()
        child.Meta.model = _ChildMetaModel
        child.create.side_effect = [
            Model.ValidationError('first failed'),
            'second',
        ]

        serializer = ListSerializer(child=child)

        with self.assertRaises(Model.ValidationError) as ctx:
            serializer.create([{}, {}])

        self.assertListEqual(ctx.exception.get_full_details(), [
            {'detail': 'first failed'},
            None,
        ])

    def test_create_raises_detail_when_second_item_fails(self):
        child = MagicMock()
        child.Meta.model = _ChildMetaModel
        child.create.side_effect = [
            'first',
            Model.ValidationError('second failed'),
        ]

        serializer = ListSerializer(child=child)

        with self.assertRaises(Model.ValidationError) as ctx:
            serializer.create([{}, {}])

        self.assertListEqual(ctx.exception.get_full_details(), [
            None,
            {'detail': 'second failed'},
        ])

    def test_create_raises_detail_when_all_items_fail(self):
        child = MagicMock()
        child.Meta.model = _ChildMetaModel
        child.create.side_effect = [
            Model.ValidationError('a'),
            Model.ValidationError('b'),
        ]

        serializer = ListSerializer(child=child)

        with self.assertRaises(Model.ValidationError) as ctx:
            serializer.create([{}, {}])

        self.assertListEqual(ctx.exception.get_full_details(), [
            {'detail': 'a'},
            {'detail': 'b'},
        ])

    def test_create_propagates_non_validation_errors(self):
        child = MagicMock()
        child.Meta.model = _ChildMetaModel
        child.create.side_effect = ValueError('not a validation error')

        serializer = ListSerializer(child=child)

        with self.assertRaises(ValueError):
            serializer.create([{}])
