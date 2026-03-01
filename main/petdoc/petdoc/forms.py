from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    fullName = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmPassword = forms.CharField(widget=forms.PasswordInput)
    country = forms.CharField(required=True)
    marketingCheck = forms.BooleanField(required=False)
    termsCheck = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['fullName', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirmPassword")

        if password != confirm:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['fullName'],
            email=self.cleaned_data['email'],
            
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user