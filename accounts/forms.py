from django import forms
from django.contrib.auth.models import User
from Store.models import Customer
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    second_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=255)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise ValidationError("Passwords do not match")
        return cleaned

    def save(self):
        email = self.cleaned_data['email']

        # Create Django user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=self.cleaned_data['password1']
        )

        # Create Customer
        Customer.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            second_name=self.cleaned_data['second_name'],
            email=email,
            phone=self.cleaned_data['phone'],
            birth_date=self.cleaned_data['birth_date'],
        )

        return user
