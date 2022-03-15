from django import forms
from .models import FibModel


class FibForm(forms.ModelForm):
    class Meta:
        model = FibModel
        fields = ['input']
        exclude_fields = 'output'
