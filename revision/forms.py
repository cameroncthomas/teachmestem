from allauth.account.forms import SignupForm
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import TutoringContactUser


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


class TutoringContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = TutoringContactUser
        fields = ["tutor_name", "first_name", "last_name", "email", "message"]
        labels = {
            "tutor_name": "Tutor name",
            "email": "Email address",
            "message": "Message",
        }
        widgets = {"text": forms.Textarea(attrs={"style": "height:150px"})}
