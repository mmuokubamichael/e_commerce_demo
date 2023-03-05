from django import forms
from django.forms import ModelForm
from .models import Shipping_adress,billing_adress
from django_countries.widgets import CountrySelectWidget


class Shipping_address_form(ModelForm):
    
    class Meta:
        model= Shipping_adress
        fields=('nationality','city','apt_suit','zipcode','default')
        labels = {'default':'set as default address'}
        widgets = {
           'city':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':'Town / City'
           }),
           'apt_suit':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':"Street address"
           }),
           'zipcode':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':'Postcode / Zip'
           }),
           'default':forms.CheckboxInput(attrs={
            'id':'address',
           }),
          
        }

class billing_address_form(ModelForm):
    
    class Meta:
        model= billing_adress
        fields=('nationality','city','apt_suit','zipcode','payment_types','first_name','last_name','email','company')
        widgets = {
           'payment_types': forms.RadioSelect(),
           'first_name':forms.TextInput(attrs={
            'class':'input-text'
           }),
           'last_name':forms.TextInput(attrs={
            'class':'input-text'
           }),
           'email':forms.EmailInput(attrs={
            'class':'input-text'
           }),
           'city':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':'Town / City'
           }),
           'apt_suit':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':"Street address"
           }),
           'zipcode':forms.TextInput(attrs={
            'class':'input-text',
            'placeholder':'Postcode / Zip'
           }),
           'company':forms.TextInput(attrs={
            'class':'input-text',
            
           }),
          
        }
        