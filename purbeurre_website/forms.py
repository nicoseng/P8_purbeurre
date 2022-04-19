from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class AccountCreationForm(forms.Form):
    pseudo = forms.CharField(max_length=100, required=True)
    nom = forms.CharField(max_length=100, required=True)
    prenom = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=200)
    mdp = forms.CharField(min_length=6, max_length=100, widget=forms.PasswordInput())

    def clean_pseudo(self):
        pseudo = self.cleaned_data.get("pseudo")
        if "$" in pseudo:
            raise forms.ValidationError("Le pseudo ne peut pas contenir de $")
        return pseudo


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SearchForm(forms.Form):
    search_product_name = forms.CharField(max_length=100, required=True)