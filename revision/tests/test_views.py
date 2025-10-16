from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from revision.models import ExamBoard, Qualification, Subject

User = get_user_model()


class qualificationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )
        number_of_subjects = 7
        qualification = Qualification.objects.get(id=1)
        for subject_id in range(1, number_of_subjects + 1):
            Subject.objects.create(
                qualification=qualification,
                name="Maths",
                subject_number=number_of_subjects - subject_id + 1,
            )
        User.objects.create_user(
            username="jdoe137",
            email="test@email.com",
            password="password137",
            first_name="John",
            last_name="Doe",
        )

    def test_redirects_if_not_logged_in(self):
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        self.assertRedirects(response, f"/accounts/login/?next=/{qualification.slug}/")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(f"/{qualification.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")

    def test_view_url_accessible_by_name(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")

    def test_view_uses_correct_template(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTemplateUsed(response, "revision/qualification.html")

    def test_lists_all_qualifications(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTrue("qualifications" in response.context)
        self.assertEqual(len(response.context["qualifications"]), 5)

    def test_qualifications_ordered_by_qualification_number(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        expected_qualification_order = sorted(
            Qualification.objects.all(), key=lambda q: q.qualification_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTrue("qualifications" in response.context)
        self.assertQuerySetEqual(
            response.context["qualifications"], expected_qualification_order
        )

    def test_lists_all_subjects(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTrue("subjects" in response.context)
        self.assertEqual(len(response.context["subjects"]), 7)

    def test_subjects_ordered_by_subject_number(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:qualification",
                kwargs={"qualification_slug": qualification.slug},
            )
        )
        expected_subject_order = sorted(
            Subject.objects.all(), key=lambda s: s.subject_number
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTrue("subjects" in response.context)
        self.assertQuerySetEqual(response.context["subjects"], expected_subject_order)


class subjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_qualifications = 5
        for qualification_id in range(1, number_of_qualifications + 1):
            Qualification.objects.create(
                name=f"Qualification {qualification_id}",
                qualification_number=number_of_qualifications - qualification_id + 1,
            )
        qualification = Qualification.objects.get(id=1)
        Subject.objects.create(
            qualification=qualification, name="Computer Science", subject_number=1
        )
        subject = Subject.objects.get(id=1)
        number_of_examboards = 7
        for examboard_id in range(1, number_of_examboards + 1):
            ExamBoard.objects.create(
                subject=subject,
                name=f"Examboard {examboard_id}",
            )
        User.objects.create_user(
            username="jdoe137",
            email="test@email.com",
            password="password137",
            first_name="John",
            last_name="Doe",
        )

    def test_redirects_if_not_logged_in(self):
        qualification = Qualification.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:subject",
                kwargs={
                    "qualification_slug": qualification.slug,
                    "subject_id": subject.id,
                    "subject_slug": subject.slug,
                },
            )
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/{qualification.slug}/{subject.id}/{subject.slug}/",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        response = self.client.get(
            f"/{qualification.slug}/{subject.id}/{subject.slug}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")

    def test_view_url_accessible_by_name(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:subject",
                kwargs={
                    "qualification_slug": qualification.slug,
                    "subject_id": subject.id,
                    "subject_slug": subject.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")

    def test_view_uses_correct_template(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:subject",
                kwargs={
                    "qualification_slug": qualification.slug,
                    "subject_id": subject.id,
                    "subject_slug": subject.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTemplateUsed(response, "revision/subject.html")

    def test_lists_all_examboards(self):
        self.client.login(username="jdoe137", password="password137")
        qualification = Qualification.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        response = self.client.get(
            reverse(
                "revision:subject",
                kwargs={
                    "qualification_slug": qualification.slug,
                    "subject_id": subject.id,
                    "subject_slug": subject.slug,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "jdoe137")
        self.assertTrue("examboards" in response.context)
        self.assertEqual(len(response.context["examboards"]), 7)
