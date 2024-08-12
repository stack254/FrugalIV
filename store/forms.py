
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class SignupForm(UserCreationForm):

    username = forms.CharField(widget= forms.TextInput(attrs={
            'required':'',
            'name': 'username',
            'class': 'form-control mb-3 p-4',
            'id': 'exampleInputName',
            'type': 'text',
            'placeholder': 'Your Username'

        }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'required': '',
        'name': 'email',
        'class': 'form-control mb-3 p-4',
        'id': 'exampleInputEmail1',
        'type': 'email',
        'placeholder': 'Your email address'

    }))


    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': '',
        'name': 'password',
        'class': 'form-control mb-3 p-4',
        'id': 'inputPassword1',
        'type': 'password',
        'placeholder': 'Set your password',


    }))


    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': '',
        'name': 're_password',
        'class': 'form-control mb-3 p-4',
        'id': 'inputPassword2',
        'type': 'password',
        'placeholder': 'Repeat Your Password'

    }))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class LoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'required': '',
        'name': 'email',
        'class': 'form-control mb-3 p-4',
        'id': 'exampleInputEmail1',
        'type': 'email',
        'placeholder': 'Enter email address'

    }))


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': '',
        'name': 'password',
        'class': 'form-control mb-3 p-4',
        'id': 'password',
        'type': 'password',
        'placeholder': 'Password',


    }))

