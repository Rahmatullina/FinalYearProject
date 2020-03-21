from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# from .models import RegionModel
# from .models import SERVICE_CHOICES, REGION_CHOICES
from django.contrib.auth import authenticate
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','type':'password'}),max_length=100)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid or user is inactive. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


# class PassResetForm(PasswordResetForm):
#     email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email',
#                                                              'type':'email'}), max_length=100)
#
#
# class PassResetConfirmForm(SetPasswordForm):
#     new_password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
#                                                                  'placeholder':'Enter new password',
#                                                                  'type':'password'}), max_length=100)
#     new_password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
#                                                                  'placeholder': 'Enter new password again',
#                                                                  'type': 'password'}), max_length=100)


# class CustomUserCreationForm(UserCreationForm):
#
#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('region_name',)
#
#
# class CustomUserChangeForm(UserChangeForm):
#     email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254)
#
#     class Meta:
#         model = CustomUser
#         fields = ('email','username')
