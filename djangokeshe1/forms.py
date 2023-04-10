from django import forms
from django.contrib.auth.forms import UserCreationForm
from .model import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number', 'username', 'password', 'is_premium', 'email', 'chat_count')
