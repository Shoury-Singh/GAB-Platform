from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your email'
    }))
    role = forms.ChoiceField(choices=User.Role.choices, required=True, widget=forms.Select(attrs={
        'class': 'form-select', 'id': 'id_role'
    }))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone number (optional)'
    }))
    business_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Your business / shop / factory name'
    }))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'City'
    }))
    state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'State'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'business_name', 'city', 'state', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create a strong password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        business_name = cleaned_data.get('business_name')
        if role in [User.Role.INDUSTRY, User.Role.WHOLESALER, User.Role.SHOPKEEPER]:
            if not business_name or not business_name.strip():
                self.add_error('business_name', "Business name is required for Industry, Wholesaler and Shopkeeper roles.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone = self.cleaned_data.get('phone', '')
        user.business_name = self.cleaned_data.get('business_name', '')
        user.city = self.cleaned_data.get('city', '')
        user.state = self.cleaned_data.get('state', '')
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username or Email', 'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username or Email"
