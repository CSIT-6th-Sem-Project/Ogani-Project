from django import forms
from crispy_forms.helper import FormHelper
from django.core import validators

class OrderForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False  # donot show crispy tag labels
        self.helper.form_show_errors = True

    CASH_ON_DELIVERY = 'cash-on-delivery'
    EPAYMENT = 'e-payment'

    PAYMENT_CHOICES = (
        (CASH_ON_DELIVERY, 'Cash on Delivery'),
        (EPAYMENT, "E-payment")
    )
    attr = {'class':'form-control'}
    first_name = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs=attr))
    last_name = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs=attr))
    email = forms.EmailField(widget=forms.EmailInput(attrs=attr),required=True,max_length=300,validators=[validators.EmailValidator(message='enter a valid email address')])
    city = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs=attr))
    address = forms.CharField(required=True,max_length=500,widget=forms.TextInput(attrs=attr))
    phone = forms.CharField(widget=forms.TextInput(attrs=attr),max_length=10,validators=[validators.RegexValidator(regex="^98[0-9]{8}",message="enter a valid phone number")],required=True)
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(attrs=attr.update({'class':'form-check-input'})),choices=PAYMENT_CHOICES,required=True)
    shipping_address = forms.CharField(required=False,max_length=500,widget=forms.TextInput(
        attrs= {'placeholder':"Shipping address (Full)",
    "class":"form-control",
    "id":"ship-diff"}
    ))

    order_notes = forms.CharField(required=False,max_length=500,widget=forms.TextInput(
        attrs={"placeholder":"Notes about your order, e.g. special notes for delivery."}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@gmail' not in email:
            raise forms.ValidationError('only gmail is accepted')
        return email