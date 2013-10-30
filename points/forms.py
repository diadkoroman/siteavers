# -*- coding:utf-8 -*-
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator

class ChooserForm(forms.Form):
    co_from = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10000)])
    co_to = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10000)])
    ci_from = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10000)])
    ci_to = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10000)])
    tr_amount = forms.IntegerField(max_value = 200000, required = False)
