from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

# exceptions
from api.framework.exceptions import AlreadyExists


class TestAlreadyExists(TestCase):
    def setUp(self):
        self.instance = AlreadyExists()

    def test_exception(self):
        self.assertIsInstance(self.instance, APIException)
        self.assertEqual(str(self.instance.detail), _('Already exists.'))
        self.assertDictEqual(self.instance.get_full_details(), {
            'message': _('Already exists.'),
            'code': 'already_exists',
        })
