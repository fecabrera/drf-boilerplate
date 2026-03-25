from unittest import mock
from django.test import TestCase
from api.framework.db import models
from django.db import models as django_models


class Model(models.Model):
    class Meta:
        app_label = 'api'
    
    created_at = models.DateTimeField(auto_now_add=True)


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
