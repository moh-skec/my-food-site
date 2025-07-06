from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    """
    Extended user creation form with additional fields and styling.
    """

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'style': 'border-radius: 15px; border: 2px solid #e9ecef; transition: all 0.3s ease;'
            })

        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a strong password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'


class LoginForm(AuthenticationForm):
    """
    Custom login form with enhanced styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'style': 'border-radius: 15px; border: 2px solid #e9ecef; transition: all 0.3s ease;'
            })

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
            'autofocus': True
        })
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'

        self.fields['username'].label = ''
        self.fields['password'].label = ''
