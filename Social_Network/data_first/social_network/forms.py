#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import User

from django import forms

class UserForm(forms.ModelForm):
    #password=forms.CharField(widget=forms.p)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name','birth_date','gender','mobile_number']

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this email, raise an error.
        raise forms.ValidationError("This email address is already in use.")



    # 'birth_date','gender','mobile_number'
