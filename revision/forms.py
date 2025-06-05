from allauth.account.forms import SignupForm
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


class RevisionSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    field_order = [
        "email",
        "email2",  # ignored when not present
        "username",
        "password1",
        "password2",  # ignored when not present
        "captcha",
    ]

    def save(self, request):
        user = super().save(request)
        return user
