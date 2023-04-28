from django import forms
from django.db.models import fields
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("name", 'email', 'text', "foto")

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )
    
    class Meta:
        model = Rating
        fields = ("star",)
