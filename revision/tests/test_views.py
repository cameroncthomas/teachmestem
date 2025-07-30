from django.test import TestCase
from django.urls import reverse

from revision.models import Qualification


class indexViewTest(TestCase):

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
        response = self.client.get(reverse("revision:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("revision:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "revision/index.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("revision:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("revision:index"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )


class privacyViewTest(TestCase):

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
        response = self.client.get(reverse("revision:privacy"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("revision:privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "revision/privacy.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("revision:privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("revision:privacy"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )
