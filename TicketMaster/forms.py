from django import forms
from .models import FavouriteEvent
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Define a form class for the Product model
class FavouriteEventsForm(forms.ModelForm):
    class Meta:
        # Specify the model associated with this form
        model = FavouriteEvent
        # Include all fields of the Product model in the form
        exclude = ['user']





# This form is not currently used, but I included in case you need to design a custom UserRegistrationForm where
# you can ask the user to enter email and password instead of password and username to register your site
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        #fields = ['username', 'email', 'password1', 'password2']
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']