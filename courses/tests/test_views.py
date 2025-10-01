import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from revision.models import ExamBoard, Qualification, Subject


class coursesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )
        qualification = Qualification.objects.get(id=1)
        subject_1 = Subject.objects.create(
            qualification=qualification, name="Physics", subject_number=1
        )
        subject_2 = Subject.objects.create(
            qualification=qualification, name="Maths", subject_number=2
        )
        examboard_1 = ExamBoard.objects.create(subject=subject_1, name="AQA")
        examboard_2 = ExamBoard.objects.create(subject=subject_2, name="AQA")
        user = User.objects.create_user(
            username="test-username",
            email="test-email@email.com",
            password="test-password",
            first_name="test-firstname",
            last_name="test-lastname",
        )
        number_of_courses = 8
        for course_id in range(1, (number_of_courses // 2) + 1):
            Course.objects.create(
                examboard=examboard_1,
                instructor=user,
                date=datetime.date(2025, 9, number_of_courses - course_id + 1),
                price=137.14,
            )
            Course.objects.create(
                examboard=examboard_2,
                instructor=user,
                date=datetime.date(2025, 9, number_of_courses - course_id + 1),
                price=137.14,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("courses:courses"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("courses:courses"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/courses.html")

    def test_lists_all_qualifications(self):
        response = self.client.get(reverse("courses:courses"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        response = self.client.get(reverse("courses:courses"))
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )

    def test_lists_all_courses(self):
        response = self.client.get(reverse("courses:courses"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("courses" in response.context)
        self.assertEqual(len(response.context["courses"]), 8)

    def test_courses_ordered_by_course_date_then_subject_name(self):
        response = self.client.get(reverse("courses:courses"))
        expected_course_order = sorted(
            Course.objects.all(), key=lambda c: (c.date, c.examboard.subject.name)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("courses" in response.context)
        self.assertQuerySetEqual(response.context["courses"], expected_course_order)
