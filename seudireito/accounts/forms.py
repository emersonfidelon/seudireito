# coding=utf-8

from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['name','email']

class UserAdminCreationForm(UserCreationForm):
    
    class Meta:
        model: User
        fields: ['name', 'email']

class UserAdminForm(forms.ModelForm):
    
    class Meta:
        model: User
        fields: ['name','email','username','is_active','is_staff','is_lawier','is_company']