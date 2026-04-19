from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address', 'class': 'form-control', 'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'class': 'form-control'
    }))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}))
    organization_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'School / College name', 'class': 'form-control'}))
    organization_type = forms.ChoiceField(choices=[
        ('school','School'),('college','College'),('university','University'),('coaching','Coaching Institute')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password (min 8 chars)', 'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'organization_name', 'organization_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0] + '_' + str(User.objects.count())
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.organization_name = self.cleaned_data['organization_name']
        user.organization_type = self.cleaned_data['organization_type']
        user.role = 'owner'
        if commit:
            user.save()
        return user
