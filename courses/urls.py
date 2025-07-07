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
    # Page that shows course registration info and form.
    path(
        "<int:course_id>/register/",
        views.courses_register,
        name="courses_register",
    ),
    # Page that shows course registration form success message.
    path(
        "<int:course_id>/register/success/",
        views.courses_register_success,
        name="courses_register_success",
    ),
]
