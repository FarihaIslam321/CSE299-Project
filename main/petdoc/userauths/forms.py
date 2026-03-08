# userauths/forms.py
from django import forms
from userauths.models import User
from django.core.exceptions import ValidationError
from core.models import  Address, Review, PaymentMethod, Product

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
            bio=f"Country: {self.cleaned_data['country']}"
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user'] 


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        exclude = ['user'] 


        
class ReviewForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),  # or filter to only products the user purchased
        empty_label="Select a product",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }