from django import forms
from django.test import TestCase

from revision.forms import ContactForm


class ContactFormTest(TestCase):

    def test_form_has_expected_fields(self):
        form = ContactForm()
        expected_fields = {"first_name", "last_name", "email", "text", "captcha"}
        self.assertSetEqual(set(form.fields.keys()), expected_fields)

    def test_form_has_expected_field_order(self):
        form = ContactForm()
        expected_field_order = ["first_name", "last_name", "email", "text", "captcha"]
        self.assertListEqual(form.field_order, expected_field_order)

    def test_first_name_label(self):
        form = ContactForm()
        self.assertEqual(form.fields["first_name"].label, "First name")

    def test_last_name_label(self):
        form = ContactForm()
        self.assertEqual(form.fields["last_name"].label, "Last name")

    def test_email_label(self):
        form = ContactForm()
        self.assertEqual(form.fields["email"].label, "Email address")

    def test_text_label(self):
        form = ContactForm()
        self.assertEqual(form.fields["text"].label, "Message")

    def test_text_field_widget_is_textarea(self):
        form = ContactForm()
        self.assertIsInstance(form.fields["text"].widget, forms.Textarea)

    def test_text_field_widget_height(self):
        form = ContactForm()
        self.assertEqual(form.fields["text"].widget.attrs.get("style"), "height:150px")
