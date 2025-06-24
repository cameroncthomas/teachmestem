from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class ContactUser(models.Model):
    """A user who contacts via the Contact Form."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.first_name} {self.last_name}"


class Qualification(models.Model):
    """A qualification one may be studying."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="default", unique=True)
    qualification_number = models.IntegerField()

    def save(self, *args, **kwargs):
        """Update slug field and save model instance."""
        self.slug = slugify(self.name)
        super(Qualification, self).save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"


class Subject(models.Model):
    """A subject for a given qualification (Qualification instance)."""

    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="default")
    subject_number = models.IntegerField()

    def save(self, *args, **kwargs):
        """Update slug field and save model instance."""
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"


class ExamBoard(models.Model):
    """An exam board for a given subject (Subject instance)."""

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="default")

    def save(self, *args, **kwargs):
        """Update slug field and save model instance."""
        self.slug = slugify(self.name)
        super(ExamBoard, self).save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"


class PastPaper(models.Model):
    """A past paper for a given exam board (ExamBoard instance)."""

    examboard = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    name = models.DateField(max_length=200)
    paper_number = models.IntegerField()
    paper = models.FileField(upload_to="pastpapers")
    model_answers = models.FileField(upload_to="model_answers")
    mark_scheme = models.FileField(upload_to="mark_schemes")

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"


class Topic(models.Model):
    """A topic for a given exam board (ExamBoard instance)."""

    examboard = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    maths_section = models.CharField(max_length=200, default="not applicable")
    topic_number = models.IntegerField()
    topic_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="default")
    notes = models.FileField(upload_to="notes")
    questions = models.FileField(upload_to="questions")

    def save(self, *args, **kwargs):
        """Update slug field and save model instance."""
        self.slug = slugify(f"Topic {self.topic_number} : {self.topic_name}")
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the model."""
        return f"Topic {self.topic_number} : {self.topic_name}"


class TopicCompletion(models.Model):
    """Status of a topic's completion for a given User and Topic."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the model."""
        return f"Is Topic complete? {self.is_complete}"


class PastPaperCompletion(models.Model):
    """Status of a past paper's completion for a given User and PastPaper."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pastpaper = models.ForeignKey(PastPaper, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the model."""
        return f"Is PastPaper complete? {self.is_complete}"


class ExamBoardCompletion(models.Model):
    """Progress in exam board (in the topics and past papers)
    for a given User and ExamBoard.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    examboard = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)

    @property
    def topics(self):
        """Return all Topic instances for a given ExamBoard."""
        return Topic.objects.filter(examboard=self.examboard)

    @property
    def pastpapers(self):
        """Return all PastPaper instances for a given ExamBoard."""
        return PastPaper.objects.filter(examboard=self.examboard)

    @property
    def completed_topics(self):
        """Return all completed topics (as Topic instances)
        for a given User and ExamBoard.
        """
        completed_topics_ids = TopicCompletion.objects.filter(
            user=self.user, topic__examboard=self.examboard, is_complete=True
        ).values("topic")
        return Topic.objects.filter(id__in=completed_topics_ids)

    @property
    def completed_pastpapers(self):
        """Return all completed past papers (as PastPaper instances)
        for a given User and ExamBoard.
        """
        completed_pastpapers_ids = PastPaperCompletion.objects.filter(
            user=self.user, pastpaper__examboard=self.examboard, is_complete=True
        ).values("pastpaper")
        return PastPaper.objects.filter(id__in=completed_pastpapers_ids)

    @property
    def is_examboard_in_my_subjects(self):
        """Return True if ExamBoard has been added to 'My Subjects' by User and
        False if not.
        """
        examboard_in_my_subjects = True
        try:
            UserExamBoard.objects.get(user=self.user, examboard=self.examboard)
        except UserExamBoard.DoesNotExist:
            examboard_in_my_subjects = False

        return examboard_in_my_subjects

    def __str__(self):
        """Return a string representation of the model."""
        return "ExamBoard completion summary"


class UserExamBoard(models.Model):
    """An ExamBoard added to 'My Subjects' by User."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    examboard = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)

    @property
    def topic_progress_percentage(self):
        """Return percentage progress in topics for a given User and
        ExamBoard instance.
        """
        num_topics_completed = TopicCompletion.objects.filter(
            user=self.user, topic__examboard=self.examboard, is_complete=True
        ).count()
        total_num_topics = Topic.objects.filter(examboard=self.examboard).count()
        return (
            int(100 * num_topics_completed / total_num_topics)
            if total_num_topics > 0
            else 0
        )

    def __str__(self):
        """Return a string representation of the model."""
        return "ExamBoard added to 'My Subjects'"
