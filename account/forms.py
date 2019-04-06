from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email",required=True, widget=forms.EmailInput())
    first_name = forms.CharField(label="First name",required=True, max_length=150, help_text="The max length of the text is 150.")
    last_name = forms.CharField(label="Last name",required=True, max_length=150, help_text="The max length of the text is 150.")

    class Meta:
        model = User
        fields = ["username", "first_name","last_name", "email"]
