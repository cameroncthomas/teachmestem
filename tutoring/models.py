from django.contrib.auth.models import User
from django.db import models


class Tutor(models.Model):
    """A user who is a tutor."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"


class TutoringContactUser(models.Model):
    """A user who contacts via the Tutoring Contact Form."""

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.first_name} {self.last_name}"
