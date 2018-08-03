import re

from django.contrib.auth import forms
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from register.models import Register

class loginForm(forms.Form):
    username = forms.CharField(max_length=30,)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,min_length=1)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(),max_length=15, min_length=3)
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput(),max_length=15, min_length=3)
    mobileNo = forms.CharField(label='Mobile No.', max_length=15, min_length=5)
    email = forms.EmailField(label='Email')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only containalphanumericcharacters and the underscore.')
        try:
            Register.objects.get(name=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')