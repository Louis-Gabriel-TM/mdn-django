import datetime

from django import forms
from django.core.exceptions import ValidationError


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Entrez une date entre aujourd'hui et dans 4 semaines (3 semaines par défaut)"
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError("Date invalide - date passée")

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError("Date invalide - date dans plus de 4 semaines")

        return data
