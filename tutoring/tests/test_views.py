from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from revision.models import Qualification
from tutoring.models import Tutor


class tutoringViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )
        number_of_tutors = 7
        for tutor_id in range(1, number_of_tutors + 1):
            user = User.objects.create_user(
                username=f"username-{tutor_id}",
                email=f"email-{tutor_id}@test.com",
                password=f"password-{tutor_id}",
                first_name=f"firstname-{tutor_id}",
                last_name=f"lastname-{tutor_id}",
            )
            Tutor.objects.create(
                user=user,
                name=f"tutor-name-{tutor_id}",
                text=f"tutor-text-{tutor_id}",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/tutoring/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("tutoring:tutoring"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("tutoring:tutoring"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tutoring/tutoring.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("tutoring:tutoring"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("tutoring:tutoring"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )

    def test_lists_all_tutors(self):
        response = self.client.get(reverse("tutoring:tutoring"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("tutors" in response.context)
        self.assertEqual(len(response.context["tutors"]), 7)
