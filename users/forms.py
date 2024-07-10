from django.contrib.auth.forms import UserCreationForm
from users.models import User
from catalog.forms import StyleFormMixin
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar', 'token')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['token'].widget = forms.HiddenInput()
