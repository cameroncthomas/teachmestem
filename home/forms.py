from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import ContactUser


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
