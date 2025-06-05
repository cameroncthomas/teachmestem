"""Defines URL patterns for tutoring."""

from django.urls import path

from . import views

app_name = "tutoring"

urlpatterns = [
    # Page that shows tutoring info.
    path(
        "",
        views.tutoring,
        name="tutoring",
    ),
    # Page that shows tutoring contact info.
    path(
        "contact/",
        views.tutoring_contact,
        name="tutoring_contact",
    ),
]
