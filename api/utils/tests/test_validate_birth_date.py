from datetime import date

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.utils.validators import validate_birth_date


@freeze_time('2020-01-01')
class TestValidateBirthDate(TestCase):
    def setUp(self):
        self.today = date.today()

    def test_validate_birth_date_19(self):
        validate_birth_date(self.today - relativedelta(years=19), 18)

    def test_validate_birth_date_18(self):
        validate_birth_date(self.today - relativedelta(years=18), 18)

    def test_validate_birth_date_17(self):
        with self.assertRaises(ValidationError) as e:
            validate_birth_date(self.today - relativedelta(years=17), 18)
        self.assertEqual(e.exception.message, _('Invalid birth date.'))

    def test_validate_birth_date_15(self):
        validate_birth_date(self.today - relativedelta(years=15), 14)

    def test_validate_birth_date_14(self):
        validate_birth_date(self.today - relativedelta(years=14), 14)

    def test_validate_birth_date_13(self):
        with self.assertRaises(ValidationError) as e:
            validate_birth_date(self.today - relativedelta(years=13), 14)
        self.assertEqual(e.exception.message, _('Invalid birth date.'))
