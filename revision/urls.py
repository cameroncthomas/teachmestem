"""Defines URL patterns for revision."""

from django.urls import path

from . import views

app_name = "revision"
urlpatterns = [
    # Home page.
    path("", views.index, name="index"),
    # Page that shows tutoring info.
    path(
        "tutoring/",
        views.tutoring,
        name="tutoring",
    ),
    # Page that shows tutoring contact form.
    path(
        "tutoring/contact/",
        views.tutoring_contact,
        name="tutoring_contact",
    ),
    # Page that shows privacy info.
    path(
        "privacy/",
        views.privacy,
        name="privacy",
    ),
    # Page that shows terms info.
    path(
        "terms/",
        views.terms,
        name="terms",
    ),
    # Page that shows 'My Subjects' for logged in users.
    path(
        "my-subjects/",
        views.my_subjects,
        name="my_subjects",
    ),
    # Page that shows options relating to account for logged in users.
    path("my-account/", views.my_account, name="my_account"),
    # Page that shows subjects for a given qualification.
    path(
        "<slug:qualification_slug>/",
        views.qualification,
        name="qualification",
    ),
    # Page that show exam boards for a given subject.
    path(
        "<slug:qualification_slug>/<int:subject_id>/<slug:subject_slug>/",
        views.subject,
        name="subject",
    ),
    # Page that shows links to revision notes, questions, and past papers for a given exam board.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<int:examboard_id>/<slug:examboard_slug>/",
        views.examboard,
        name="examboard",
    ),
    # Page that shows notes belonging to a topic.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<slug:examboard_slug>/<int:topic_id>/<slug:topic_slug>/notes/",
        views.notes,
        name="notes",
    ),
    # Page that shows questions belonging to a topic.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<slug:examboard_slug>/<int:topic_id>/<slug:topic_slug>/questions/",
        views.questions,
        name="questions",
    ),
    # Page that shows a past paper belonging to an exam board.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<slug:examboard_slug>/<int:pastpaper_id>/<str:pastpaper_name>/past-paper/",
        views.past_paper,
        name="past_paper",
    ),
    # Page that shows a past paper's model answers.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<slug:examboard_slug>/<int:pastpaper_id>/<str:pastpaper_name>/model-answers/",
        views.model_answers,
        name="model_answers",
    ),
    # Page that shows a past paper's official mark scheme.
    path(
        "<slug:qualification_slug>/<slug:subject_slug>/<slug:examboard_slug>/<int:pastpaper_id>/<str:pastpaper_name>/mark-scheme/",
        views.mark_scheme,
        name="mark_scheme",
    ),
    # Page for marking a topic as complete.
    path(
        "complete_topic/<int:topic_id>/",
        views.mark_topic_as_complete,
        name="mark_topic_as_complete",
    ),
    # Page for marking a topic as uncomplete.
    path(
        "uncomplete_topic/<int:topic_id>/",
        views.mark_topic_as_uncomplete,
        name="mark_topic_as_uncomplete",
    ),
    # Page for marking a past paper as complete.
    path(
        "complete_pastpaper/<int:pastpaper_id>/",
        views.mark_pastpaper_as_complete,
        name="mark_pastpaper_as_complete",
    ),
    # Page for marking a past paper as uncomplete.
    path(
        "uncomplete_pastpaper/<int:pastpaper_id>/",
        views.mark_pastpaper_as_uncomplete,
        name="mark_pastpaper_as_uncomplete",
    ),
    # Page for adding an exam board to 'My Subjects'.
    path(
        "add_examboard_to_my_subjects/<int:examboard_id>/",
        views.add_examboard_to_my_subjects,
        name="add_examboard_to_my_subjects",
    ),
    # Page for removing an exam board from 'My Subjects'.
    path(
        "remove_examboard_from_my_subjects/<int:examboard_id>/",
        views.remove_examboard_from_my_subjects,
        name="remove_examboard_from_my_subjects",
    ),
]
