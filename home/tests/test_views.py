from django.test import TestCase
from django.urls import reverse

from revision.models import Qualification


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("home:index"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )


class PrivacyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/privacy/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home:privacy"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home:privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/privacy.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("home:privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("home:privacy"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )


class TermsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/terms/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home:terms"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home:terms"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/terms.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("home:terms"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("home:terms"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )


class ContactViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home:contact"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("home:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("home:contact"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )


class ContactSentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/contact/sent/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home:contact_sent"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home:contact_sent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact_sent.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("home:contact_sent"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("home:contact_sent"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )
