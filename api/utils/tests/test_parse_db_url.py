from django.test import TestCase

from api.utils.settings import parse_db_url


class TestParseDBURL(TestCase):
    def test_parse_db_url_none(self):
        result = parse_db_url(None)
        self.assertEqual(result, {})

    def test_parse_db_url_no_match(self):
        result = parse_db_url('invalid_url')
        self.assertEqual(result, {})

    def test_parse_db_url(self):
        result = parse_db_url('postgres://user:password@host:5432/dbname')
        self.assertEqual(result, {
            'protocol': 'postgres',
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': '5432',
            'name': 'dbname',
        })
