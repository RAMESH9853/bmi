from django import forms
from django.contrib.auth.forms import authenticate,UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True)

    class Meta:
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned
        self('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Your account is inactive.')
        self.check_for_test_cookie()
        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()

    def get_users(self, email):
        return User.objects.filter(email=email, is_active=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('There is no user registered with the specified email address!')
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text="Enter a strong password with at least 8 characters.",
    )
    new_password2 = forms.CharField(
        label='Confirm password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
