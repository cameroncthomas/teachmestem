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
        "<int:tutor_id>/contact/",
        views.tutoring_contact,
        name="tutoring_contact",
    ),
    # Page that shows tutoring contact form success message.
    path(
        "<int:tutor_id>/contact/sent/",
        views.tutoring_contact_sent,
        name="tutoring_contact_sent",
    ),
]
