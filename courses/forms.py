from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import CourseRegisterUser


class CourseRegisterForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = CourseRegisterUser
        fields = [
            "course",
            "first_name",
            "last_name",
            "email",
        ]
        labels = {
            "email": "Email address",
        }
