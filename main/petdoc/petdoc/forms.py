from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    country = forms.ChoiceField(choices=[('us', 'United States'), ('ca', 'Canada'), ('uk', 'United Kingdom'), 
                                        ('au', 'Australia'), ('de', 'Germany'), ('fr', 'France'), 
                                        ('jp', 'Japan'), ('other', 'Other')], required=True)
    terms_check = forms.BooleanField(required=True)
    marketing_check = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        # Ensure the email is unique
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        
        return cleaned_data