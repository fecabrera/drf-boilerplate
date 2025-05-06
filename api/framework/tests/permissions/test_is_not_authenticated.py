from unittest.mock import Mock
from rest_framework.test import APITestCase

from api.framework.permissions import IsNotAuthenticated


class TestIsNotAuthenticatedPermission(APITestCase):
    def setUp(self):
        self.permission = IsNotAuthenticated()
        self.mock_request = Mock()

    def test_permission_denied_for_authenticated_user(self):
        self.mock_request.user = Mock(is_authenticated=True)
        self.assertFalse(self.permission.has_permission(self.mock_request, None))

    def test_permission_granted_for_unauthenticated_user(self):
        self.mock_request.user = Mock(is_authenticated=False)
        self.assertTrue(self.permission.has_permission(self.mock_request, None))
