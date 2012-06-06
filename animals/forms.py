from datetime import date

from django import forms

class AnimalSearchForm(forms.Form):
    intake_date = forms.DateField(required=False)
    animal_type_choices = (
      ('', '----'),
      ('CAT', 'Cat'),
      ('DOG', 'Dog'),
    )
    animal_type = forms.ChoiceField(required=False, choices=animal_type_choices)
    sex_choices = (
      ('', '----'),
      ('M', 'Male'),
      ('F', 'Female'),
      ('S', 'Spayed'),
      ('N', 'Neutered'),
    )
    sex = forms.ChoiceField(required=False, choices=sex_choices)
