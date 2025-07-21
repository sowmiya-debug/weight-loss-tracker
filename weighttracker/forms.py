from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WeightEntry

class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight']


class SignUpForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'password1','password2' ]