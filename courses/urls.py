"""Defines URL patterns for courses."""

from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    # Page that shows courses info.
    path(
        "",
        views.courses,
        name="courses",
    ),
]
