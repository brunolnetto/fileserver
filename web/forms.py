from django.forms import ModelForm
from .models import Upload

class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['file']


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
            }),
        }
        help_texts = {
            'password1': None,  # Disable default help texts
            'password2': None,
        }