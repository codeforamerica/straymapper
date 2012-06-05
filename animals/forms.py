from datetime import date

from django import forms

class AnimalSearchForm(forms.Form):
    intake_date = forms.DateField(initial=date.today)
