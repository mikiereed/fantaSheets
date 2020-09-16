from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(
                'Email is already used by another user')
        return cd['email']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')
