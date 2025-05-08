from unittest.mock import MagicMock
from django.test import TestCase
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.framework.shortcuts import get_object_or_404, Http404


class TestGetObjectOr404(TestCase):
    def setUp(self):
        self.model = MagicMock(spec=models.Model)
        self.model.DoesNotExist = models.ObjectDoesNotExist
        self.model._meta = MagicMock(verbose_name='model')
        self.model._default_manager = MagicMock(spec=models.Manager)
        self.model._default_manager.all.return_value = self.model._default_manager
        self.model._default_manager.get.return_value = self.model
        self.model._default_manager.model = self.model

    def test_get_object_or_404(self):
        obj = get_object_or_404(self.model, id=1)
        self.assertEqual(obj, self.model)

        self.model._default_manager.get.assert_called_once_with(id=1)

    def test_get_object_or_404_no_get_method(self):
        expected_message = (
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % object.__name__
        )
        with self.assertRaisesMessage(ValueError, expected_message):
            get_object_or_404(object, id=1)

    def test_get_object_or_404_does_not_exist(self):
        self.model._default_manager.get.side_effect = self.model.DoesNotExist

        expected_message = _("No {value} matches the given query.").format(value=_('model'))
        with self.assertRaisesMessage(Http404, expected_message):
            get_object_or_404(self.model, id=1)
