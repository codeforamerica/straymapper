from django import forms

from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ('geometry',)
        widgets = {
            'location': forms.TextInput(attrs={'style': 'width:88%'}),
            'description': forms.Textarea(attrs={'rows':'7'}),
            'contact_info': forms.Textarea(attrs={'rows':'7'})
        }
