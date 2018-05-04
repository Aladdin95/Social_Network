from django.core.exceptions import ValidationError
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2',
                  'email', 'first_name', 'last_name',
                  'birth_date', 'gender', 'mobile_number']

        def save(self, commit=True):
            user = self.save(commit=False)
            user.username = self.cleaned_data['username']
            user.set_password(self.cleaned_data['first_name'])
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.birth_date = self.cleaned_data['birth_date']
            user.gender = self.cleaned_data['gender']
            user.mobile_number = self.cleaned_data['mobile_number']

            if commit:
                user.save()

            return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
