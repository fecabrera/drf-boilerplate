from unittest.mock import Mock
from django.test import TestCase
from api.framework.permissions import IsNotAuthenticatedOrReadOnly
from rest_framework.permissions import SAFE_METHODS


class TestIsNotAuthenticatedOrReadOnly(TestCase):
    def setUp(self):
        self.permission = IsNotAuthenticatedOrReadOnly()
        self.request = Mock()

    def test_authenticated_user_read_only_access(self):
        self.request.user = Mock(is_authenticated=True)
        self.request.method = 'GET'
        self.assertTrue(self.permission.has_permission(self.request, None))

    def test_authenticated_user_non_read_only_access(self):
        self.request.user = Mock(is_authenticated=True)
        self.request.method = 'POST'
        self.assertFalse(self.permission.has_permission(self.request, None))

    def test_unauthenticated_user_read_only_access(self):
        self.request.user = Mock(is_authenticated=False)
        self.request.method = 'GET'
        self.assertFalse(self.permission.has_permission(self.request, None))

    def test_unauthenticated_user_non_read_only_access(self):
        self.request.user = Mock(is_authenticated=False)
        self.request.method = 'POST'
        self.assertTrue(self.permission.has_permission(self.request, None))

    def test_safe_methods_constant_correctness(self):
        self.assertIn('GET', SAFE_METHODS)
        self.assertNotIn('POST', SAFE_METHODS)
