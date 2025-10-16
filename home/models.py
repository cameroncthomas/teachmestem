from django.db import models


class ContactUser(models.Model):
    """A user who contacts via the Contact Form."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    text = models.TextField(max_length=10000)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.first_name} {self.last_name}"
