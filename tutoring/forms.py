from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import TutoringContactUser


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
        widgets = {"message": forms.Textarea(attrs={"style": "height:150px"})}
