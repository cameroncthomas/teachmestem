from django.contrib.auth.models import User
from django.db import models

from revision.models import ExamBoard


class Course(models.Model):
    """A course ran by an instructor for a given ExamBoard instance."""

    examboard = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.examboard} course ran by {self.instructor} on {self.date}"
