from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_validators_help_text_html, validate_password
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile

AuthUser = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        # exclude = []
        fields = ('first_name', 'last_name', 'email')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validators_help_text_html()
    )
    password_confirmation = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_password(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = AuthUser(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        validate_password(password, user=user)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data['password_confirmation']

        if password is not None and password != password_confirmation:
            # Check if password is None -> in this case it means password is not validated in previous method.
            raise forms.ValidationError('Password is not confirmed!')

        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit is True:
            user.save()

        return user


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = ('first_name', 'last_name', 'email')
