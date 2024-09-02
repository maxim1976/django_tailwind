from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile


class UserInfoForm(forms.ModelForm):    
    phone = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address']

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Phone Number'})
        self.fields['address'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Address'})



class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Confirm New Password'})



class UserUpdateForm(UserChangeForm):
    password = None
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Email'})

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input mt-1 block w-full', 'placeholder': 'Confirm Password'})

