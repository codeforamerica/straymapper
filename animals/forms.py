from datetime import date

from django import forms

class AnimalSearchForm(forms.Form):
    animal_type_choices = (
      ('', ''),
      ('CAT', 'Cat'),
      ('DOG', 'Dog'),
    )
    intake_date = forms.DateField(required=False)
    animal_type = forms.ChoiceField(required=False, choices=animal_type_choices)
