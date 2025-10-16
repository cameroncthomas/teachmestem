import datetime

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.text import slugify

from revision.models import (
    ExamBoard,
    PastPaper,
    Qualification,
    Subject,
    Topic,
    TopicCompletion,
)


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


class ExamBoardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        qualification = Qualification.objects.create(
            name="GCSE", qualification_number=1
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Physics", subject_number=137
        )
        ExamBoard.objects.create(subject=subject, name="AQA")

    def test_subject_label(self):
        examboard = ExamBoard.objects.get(id=1)
        subject_label = examboard._meta.get_field("subject").verbose_name
        self.assertEqual(subject_label, "subject")

    def test_name_label(self):
        examboard = ExamBoard.objects.get(id=1)
        name_label = examboard._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_slug_label(self):
        examboard = ExamBoard.objects.get(id=1)
        slug_label = examboard._meta.get_field("slug").verbose_name
        self.assertEqual(slug_label, "slug")

    def test_name_max_length(self):
        examboard = ExamBoard.objects.get(id=1)
        name_max_length = examboard._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 200)

    def test_slug_max_length(self):
        examboard = ExamBoard.objects.get(id=1)
        slug_max_length = examboard._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 200)

    def test_save_updates_slug_field(self):
        qualification = Qualification.objects.create(
            name="A Level", qualification_number=2
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Maths", subject_number=123
        )
        examboard = ExamBoard.objects.create(subject=subject, name="OCR")
        examboard.slug = "slug"
        examboard.save()
        expected_slug = slugify(examboard.name)
        self.assertEqual(examboard.slug, expected_slug)

    def test_string_representation_is_name(self):
        examboard = ExamBoard.objects.get(id=1)
        expected_string_representation = f"{examboard.name}"
        self.assertEqual(str(examboard), expected_string_representation)


class PastPaperModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        qualification = Qualification.objects.create(
            name="IGCSE", qualification_number=271
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Computer Science", subject_number=137
        )
        examboard = ExamBoard.objects.create(subject=subject, name="AQA")
        PastPaper.objects.create(
            examboard=examboard,
            name=datetime.date(2025, 7, 24),
            paper_number=137,
            paper=ContentFile("test-paper-content", name="test-paper"),
            model_answers=ContentFile(
                "test-model-answers-content", name="test-model-answers"
            ),
            mark_scheme=ContentFile(
                "test-mark-scheme-content", name="test-mark-scheme"
            ),
        )

    def test_examboard_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        examboard_label = pastpaper._meta.get_field("examboard").verbose_name
        self.assertEqual(examboard_label, "examboard")

    def test_name_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        name_label = pastpaper._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_paper_number_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        paper_number_label = pastpaper._meta.get_field("paper_number").verbose_name
        self.assertEqual(paper_number_label, "paper number")

    def test_paper_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        paper_label = pastpaper._meta.get_field("paper").verbose_name
        self.assertEqual(paper_label, "paper")

    def test_model_answers_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        model_answers_label = pastpaper._meta.get_field("model_answers").verbose_name
        self.assertEqual(model_answers_label, "model answers")

    def test_mark_scheme_label(self):
        pastpaper = PastPaper.objects.get(id=1)
        mark_scheme_label = pastpaper._meta.get_field("mark_scheme").verbose_name
        self.assertEqual(mark_scheme_label, "mark scheme")

    def test_name_max_length(self):
        pastpaper = PastPaper.objects.get(id=1)
        name_max_length = pastpaper._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 200)

    def test_string_representation_is_name(self):
        pastpaper = PastPaper.objects.get(id=1)
        expected_string_representation = f"{pastpaper.name}"
        self.assertEqual(str(pastpaper), expected_string_representation)


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        qualification = Qualification.objects.create(
            name="A level", qualification_number=1
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Computer Science", subject_number=1
        )
        examboard = ExamBoard.objects.create(subject=subject, name="OCR")
        Topic.objects.create(
            examboard=examboard,
            topic_number=1,
            topic_name="Data Structures and Algorithms",
            notes=ContentFile("test-notes-content", name="test_files/test-notes"),
            questions=ContentFile(
                "test-questions-content", name="test_files/test-questions"
            ),
        )

    def test_examboard_label(self):
        topic = Topic.objects.get(id=1)
        examboard_label = topic._meta.get_field("examboard").verbose_name
        self.assertEqual(examboard_label, "examboard")

    def test_maths_section_label(self):
        topic = Topic.objects.get(id=1)
        maths_section_label = topic._meta.get_field("maths_section").verbose_name
        self.assertEqual(maths_section_label, "maths section")

    def test_topic_number_label(self):
        topic = Topic.objects.get(id=1)
        topic_number_label = topic._meta.get_field("topic_number").verbose_name
        self.assertEqual(topic_number_label, "topic number")

    def test_topic_name_label(self):
        topic = Topic.objects.get(id=1)
        topic_name_label = topic._meta.get_field("topic_name").verbose_name
        self.assertEqual(topic_name_label, "topic name")

    def test_slug_label(self):
        topic = Topic.objects.get(id=1)
        slug_label = topic._meta.get_field("slug").verbose_name
        self.assertEqual(slug_label, "slug")

    def test_notes_label(self):
        topic = Topic.objects.get(id=1)
        notes_label = topic._meta.get_field("notes").verbose_name
        self.assertEqual(notes_label, "notes")

    def test_questions_label(self):
        topic = Topic.objects.get(id=1)
        questions_label = topic._meta.get_field("questions").verbose_name
        self.assertEqual(questions_label, "questions")

    def test_maths_section_max_length(self):
        topic = Topic.objects.get(id=1)
        maths_section_max_length = topic._meta.get_field("maths_section").max_length
        self.assertEqual(maths_section_max_length, 200)

    def test_topic_name_max_length(self):
        topic = Topic.objects.get(id=1)
        topic_name_max_length = topic._meta.get_field("topic_name").max_length
        self.assertEqual(topic_name_max_length, 200)

    def test_slug_max_length(self):
        topic = Topic.objects.get(id=1)
        slug_max_length = topic._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 200)

    def test_save_updates_slug_field(self):
        qualification = Qualification.objects.create(
            name="IGCSE", qualification_number=3
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Maths", subject_number=314
        )
        examboard = ExamBoard.objects.create(subject=subject, name="AQA")
        topic = Topic.objects.create(
            examboard=examboard, topic_number=3, topic_name="Complex Numbers"
        )
        topic.slug = "slug"
        topic.save()
        expected_slug = slugify(f"Topic {topic.topic_number} : {topic.topic_name}")
        self.assertEqual(topic.slug, expected_slug)

    def test_string_representation_is_topic_topic_number_colon_topic_name(self):
        topic = Topic.objects.get(id=1)
        expected_string_representation = (
            f"Topic {topic.topic_number} : {topic.topic_name}"
        )
        self.assertEqual(str(topic), expected_string_representation)


class TopicCompletionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="test-username",
            email="test-email@test.com",
            password="test-password",
            first_name="test-firstname",
            last_name="test-lastname",
        )
        qualification = Qualification.objects.create(
            name="A level", qualification_number=2
        )
        subject = Subject.objects.create(
            qualification=qualification, name="Computer Science", subject_number=2
        )
        examboard = ExamBoard.objects.create(subject=subject, name="AQA")
        topic = Topic.objects.create(
            examboard=examboard,
            topic_number=1,
            topic_name="Distributed Systems",
            notes=ContentFile("test-notes-content", name="test_files/test-notes"),
            questions=ContentFile(
                "test-questions-content", name="test_files/test-questions"
            ),
        )
        TopicCompletion.objects.create(user=user, topic=topic)

    def test_user_label(self):
        topic_completion = TopicCompletion.objects.get(id=1)
        user_label = topic_completion._meta.get_field("user").verbose_name
        self.assertEqual(user_label, "user")

    def test_topic_label(self):
        topic_completion = TopicCompletion.objects.get(id=1)
        topic_label = topic_completion._meta.get_field("topic").verbose_name
        self.assertEqual(topic_label, "topic")

    def test_is_complete_label(self):
        topic_completion = TopicCompletion.objects.get(id=1)
        is_complete_label = topic_completion._meta.get_field("is_complete").verbose_name
        self.assertEqual(is_complete_label, "is complete")

    def test_string_representation_is_topic_str_completion_status(self):
        topic_completion = TopicCompletion.objects.get(id=1)
        expected_string_representation = f"{topic_completion.topic} completion status"
        self.assertEqual(str(topic_completion), expected_string_representation)
