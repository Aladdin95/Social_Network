#from django.contrib.auth.models import User
from social_network.models import User

from django import forms

class UserForm(forms.ModelForm):
    #password=forms.CharField(widget=forms.p)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name','birth_date','gender','mobile_number']
#'birth_date','gender','mobile_number'