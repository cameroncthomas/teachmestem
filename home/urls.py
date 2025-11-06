"""Defines URL patterns for home."""

from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    # Home page.
    path("", views.index, name="index"),
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
    # Page that shows contact info and form.
    path(
        "contact/",
        views.contact,
        name="contact",
    ),
    # Page that shows contact form success message.
    path(
        "contact/sent/",
        views.contact_sent,
        name="contact_sent",
    ),
    # Page that shows options relating to account for logged in users.
    path("my-account/", views.my_account, name="my_account"),
    # Page that shows pricing info.
    path("pricing/", views.pricing, name="pricing"),
]
