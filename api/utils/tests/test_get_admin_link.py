import mock
from django.test import TestCase
from django.utils.html import format_html

from api.utils.admin import get_admin_link


class TestGetAdminLink(TestCase):
    def test_get_admin_link_none(self):
        with self.assertRaises(AssertionError):
            get_admin_link(None)

    @mock.patch('api.utils.admin.resolve_url', side_effect=lambda _, obj_id: '/admin/obj/{}/'.format(obj_id))
    @mock.patch('api.utils.admin.admin_urlname')
    def test_get_admin_link(self, mock_admin_urlname, mock_resolve_url):
        obj = mock.MagicMock(id=1234)

        result = get_admin_link(obj)
        self.assertEqual(result, format_html('<a href="/admin/obj/{}/">{}</a>', obj.id, obj))
