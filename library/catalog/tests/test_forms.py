import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertEquals(
            form.fields['renewal_date'].label, 
            "Nouvelle date de retour",
        )

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEquals(
            form.fields['renewal_date'].help_text,
            "Entrez une date entre aujourd'hui et dans 4 semaines (3 semaines par défaut)",
        )

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(
            data={'renewal_date': date},
        )
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today(
            ) + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(
            data={'renewal_date': date},
        )
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(
            data={'renewal_date': date},
        )
        self.assertTrue(form.is_valid())

    def test_renew_form_max_date(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(
            data={'renewal_date': date},
        )
        self.assertTrue(form.is_valid())
