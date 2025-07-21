from django.test import TestCase
from django.utils.text import slugify

from revision.models import ContactUser, Qualification, Subject


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


class QualificationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Qualification.objects.create(name="GCSE", qualification_number=137)

    def test_name_label(self):
        qualification = Qualification.objects.get(id=1)
        name_label = qualification._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_slug_label(self):
        qualification = Qualification.objects.get(id=1)
        slug_label = qualification._meta.get_field("slug").verbose_name
        self.assertEqual(slug_label, "slug")

    def test_qualification_number_label(self):
        qualification = Qualification.objects.get(id=1)
        qualification_number_label = qualification._meta.get_field(
            "qualification_number"
        ).verbose_name
        self.assertEqual(qualification_number_label, "qualification number")

    def test_name_max_length(self):
        qualification = Qualification.objects.get(id=1)
        name_max_length = qualification._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 200)

    def test_slug_max_length(self):
        qualification = Qualification.objects.get(id=1)
        slug_max_length = qualification._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 200)

    def test_save_updates_slug_field(self):
        qualification = Qualification.objects.create(
            name="A Level", qualification_number=731
        )
        qualification.slug = "slug"
        qualification.save()
        expected_slug = slugify(qualification.name)
        self.assertEqual(qualification.slug, expected_slug)

    def test_string_representation_is_name(self):
        qualification = Qualification.objects.get(id=1)
        expected_string_representation = f"{qualification.name}"
        self.assertEqual(str(qualification), expected_string_representation)


class SubjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        qualification = Qualification.objects.create(
            name="GCSE", qualification_number=1
        )
        Subject.objects.create(
            qualification=qualification, name="Physics", subject_number=137
        )

    def test_qualification_label(self):
        subject = Subject.objects.get(id=1)
        qualification_label = subject._meta.get_field("qualification").verbose_name
        self.assertEqual(qualification_label, "qualification")

    def test_name_label(self):
        subject = Subject.objects.get(id=1)
        name_label = subject._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_slug_label(self):
        subject = Subject.objects.get(id=1)
        slug_label = subject._meta.get_field("slug").verbose_name
        self.assertEqual(slug_label, "slug")

    def test_subject_number_label(self):
        subject = Subject.objects.get(id=1)
        subject_number_label = subject._meta.get_field("subject_number").verbose_name
        self.assertEqual(subject_number_label, "subject number")

    def test_name_max_length(self):
        subject = Subject.objects.get(id=1)
        name_max_length = subject._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 200)

    def test_slug_max_length(self):
        subject = Subject.objects.get(id=1)
        slug_max_length = subject._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 200)

    def test_save_updates_slug_field(self):
        qualification = Qualification.objects.create(
            name="A Level", qualification_number=2
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Maths", subject_number=314
        )
        subject.slug = "slug"
        subject.save()
        expected_slug = slugify(subject.name)
        self.assertEqual(subject.slug, expected_slug)

    def test_string_representation_is_name(self):
        subject = Subject.objects.get(id=1)
        expected_string_representation = f"{subject.name}"
        self.assertEqual(str(subject), expected_string_representation)
