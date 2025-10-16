from home.models import ContactUser
from django.test import TestCase


class ContactUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ContactUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@email.com",
            text="This is a test contact message.",
        )

    def test_first_name_label(self):
        contact_user = ContactUser.objects.get(id=1)
        first_name_label = contact_user._meta.get_field("first_name").verbose_name
        self.assertEqual(first_name_label, "first name")

    def test_last_name_label(self):
        contact_user = ContactUser.objects.get(id=1)
        last_name_label = contact_user._meta.get_field("last_name").verbose_name
        self.assertEqual(last_name_label, "last name")

    def test_email_label(self):
        contact_user = ContactUser.objects.get(id=1)
        email_label = contact_user._meta.get_field("email").verbose_name
        self.assertEqual(email_label, "email")

    def test_text_label(self):
        contact_user = ContactUser.objects.get(id=1)
        text_label = contact_user._meta.get_field("text").verbose_name
        self.assertEqual(text_label, "text")

    def test_first_name_max_length(self):
        contact_user = ContactUser.objects.get(id=1)
        first_name_max_length = contact_user._meta.get_field("first_name").max_length
        self.assertEqual(first_name_max_length, 200)

    def test_last_name_max_length(self):
        contact_user = ContactUser.objects.get(id=1)
        last_name_max_length = contact_user._meta.get_field("last_name").max_length
        self.assertEqual(last_name_max_length, 200)

    def test_email_max_length(self):
        contact_user = ContactUser.objects.get(id=1)
        email_max_length = contact_user._meta.get_field("email").max_length
        self.assertEqual(email_max_length, 254)

    def test_text_max_length(self):
        contact_user = ContactUser.objects.get(id=1)
        text_max_length = contact_user._meta.get_field("text").max_length
        self.assertEqual(text_max_length, 10000)

    def test_string_representation_is_first_name_space_last_name(self):
        contact_user = ContactUser.objects.get(id=1)
        expected_string_representation = (
            f"{contact_user.first_name} {contact_user.last_name}"
        )
        self.assertEqual(str(contact_user), expected_string_representation)
