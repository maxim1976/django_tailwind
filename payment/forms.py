from django import forms
from . models import ShippingAddress


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_phone', 'shipping_email', 'shipping_address']
        exclude = ['user']
        widgets = {
            'shipping_full_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full', 'placeholder': 'Full Name'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full', 'placeholder': 'Phone'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full', 'placeholder': 'Email'}), 
            'shipping_address': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full', 'placeholder': 'Address'}),
        }


class PaymentForm(forms.Form):
    card_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input mt-1 block', 'placeholder': 'Card Number'}))
    card_exp_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input mt-1 block', 'placeholder': 'MM/YY'}))
    card_cvv_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input mt-1 block', 'placeholder': 'CVV'}))
    card_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input mt-1 block', 'placeholder': 'Card Holder Name'}))
    card_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input mt-1 block', 'placeholder': 'Card Holder Address'}))