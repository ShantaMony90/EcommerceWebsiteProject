from django import forms
from store.models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class DashboardForm(forms.Form):
    class Meta:
        model = DashboardInfo
        fields = ['password', 'new_password', 'confirm_password']
