from django import forms
from django.forms import fields, models
from .models import CoverLetter


class CoverletterForm(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields=['coverletter']