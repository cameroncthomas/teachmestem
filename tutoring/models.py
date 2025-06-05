from django.db import models


class TutoringContactUser(models.Model):
    """A user who contacts via the Tutoring Contact Form."""

    tutor_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.first_name} {self.last_name}"
