from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from crispy_forms.helper import FormHelper
from django.core import validators

class UserAuthForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(UserAuthForm,self).__init__(*args,**kwargs)
        #self.helper.form_show_labels = False  # donot show crispy tag labelss

    username = UsernameField(
        widget=forms.TextInput(attrs={'placeholder':'username','class':'form-control'})
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'placeholder':'password','class':'form-control'}
    ))


