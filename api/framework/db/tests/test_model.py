from unittest import mock
from django.test import TestCase
from rest_framework import status
from api.framework.db import models
from django.db import models as django_models


class Model(models.Model):
    class Meta:
        app_label = 'api'
    
    created_at = models.DateTimeField(auto_now_add=True)


class TestValidationError(TestCase):
    def test_default_status_code(self):
        self.assertEqual(Model.ValidationError.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_string_detail_stored_as_error_detail(self):
        exc = Model.ValidationError('something went wrong')
        self.assertEqual(str(exc.detail), 'something went wrong')

    def test_default_detail_used_when_no_args(self):
        exc = Model.ValidationError()
        self.assertEqual(str(exc.detail), str(Model.ValidationError.default_detail))

    def test_list_detail_stored_as_is(self):
        detail = [None, {'detail': 'error on row 2'}]
        exc = Model.ValidationError(detail)
        self.assertEqual(exc.detail, detail)

    def test_list_detail_preserves_none_slots(self):
        detail = [None, {'detail': 'error'}]
        exc = Model.ValidationError(detail)
        self.assertIsNone(exc.detail[0])

    def test_get_full_details_returns_list_directly(self):
        detail = [{'detail': 'a'}, None, {'detail': 'b'}]
        exc = Model.ValidationError(detail)
        self.assertEqual(exc.get_full_details(), detail)

    def test_get_full_details_for_string_detail(self):
        exc = Model.ValidationError('error')
        full = exc.get_full_details()
        self.assertIn('message', full)
        self.assertEqual(str(full['message']), 'error')

    def test_default_code_used_when_not_provided(self):
        exc = Model.ValidationError('error')
        self.assertEqual(exc.detail.code, Model.ValidationError.default_code)

    def test_custom_code_stored_on_detail(self):
        exc = Model.ValidationError('error', code='custom_code')
        self.assertEqual(exc.detail.code, 'custom_code')

    def test_default_code_used_when_none_passed_explicitly(self):
        exc = Model.ValidationError('error', code=None)
        self.assertEqual(exc.detail.code, Model.ValidationError.default_code)


class TestModel(TestCase):
    def setUp(self):
        self.model = Model()
    
    def test_is_valid(self):
        self.assertTrue(self.model.is_valid())
    
    def test_is_valid_w_raise_exception(self):
        self.assertTrue(self.model.is_valid(raise_exception=True))
    
    @mock.patch.object(Model, 'is_valid', return_value=True)
    @mock.patch.object(django_models.Model, 'save')
    def test_save(self, mock_save, mock_is_valid):
        self.model.save()
        mock_is_valid.assert_called_once()
    
    @mock.patch.object(Model, 'is_valid', side_effect=Model.ValidationError)
    @mock.patch.object(django_models.Model, 'save')
    def test_save_w_validation_error(self, mock_save, mock_is_valid):
        with self.assertRaises(Model.ValidationError):
            self.model.save()
        mock_is_valid.assert_called_once()
