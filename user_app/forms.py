from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from user_app.models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',]


class ProfileUpdate(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'phone', 'date_of_birth']
