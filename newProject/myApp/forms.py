# forms.py
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User  # Import the User model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'address', 'mobile', 'gender']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
