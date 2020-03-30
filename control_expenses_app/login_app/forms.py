from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account, Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        fieldnames = ['email', 'username', 'password1', 'password2']
        labels = ["Adres e-mail", "Nazwa użytkownika", "Hasło", "Powtórz hasło"]

        for fieldname, label in zip(fieldnames, labels):
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = label

    class Meta:
        model = Account
        fields = ['email','username','password1','password2']



class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ['email','password']
        
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Podane dane są nieprawidłowe")



class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'monthly_budget']
        labels = {"first_name": "Imię", "last_name": "Nazwisko", "monthly_budget": "Budżet miesięczny"}