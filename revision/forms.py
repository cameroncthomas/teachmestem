from allauth.account.forms import SignupForm
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import ContactUser


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


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    field_order = ["first_name", "last_name", "email", "text", "captcha"]

    class Meta:
        model = ContactUser
        fields = ["first_name", "last_name", "email", "text"]
        labels = {
            "email": "Email address",
            "text": "Message",
        }
        widgets = {"text": forms.Textarea(attrs={"style": "height:150px"})}
