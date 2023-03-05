from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from .models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean(self):
        data = super().clean()
        if data['confirm'] != data['password']:
            raise ValidationError({
                "confirm": _("Parollar bir xil emas!!")
            })

        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm')
        widgets = {
            'password': forms.PasswordInput
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label=_('Ism'))
    last_name = forms.CharField(required=True, label=_('Familiya'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': _('Login')
        }


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        if not check_password(self.cleaned_data.get('password'), self.user.password):
            raise ValidationError(_('Parol notogri'))
        return self.cleaned_data['password']

    def clean(self):
        data = super().clean()
        if data['new_password'] != data['confirm_password']:
            raise ValidationError({
                "confirm_password": _("Parollar bir xil emas!!")
            })

        return data
